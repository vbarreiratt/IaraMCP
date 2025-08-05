"""
Performance optimization utilities for audio processing.
"""

import asyncio
import time
import hashlib
import pickle
import tempfile
import os
import logging
from typing import Dict, Any, Optional, Callable, Tuple, List
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading
from functools import wraps, lru_cache

import numpy as np

logger = logging.getLogger(__name__)

class AudioCache:
    """LRU cache for audio analysis results with file change detection."""
    
    def __init__(self, max_size: int = 100, cache_dir: Optional[str] = None):
        """
        Initialize audio cache.
        
        Args:
            max_size: Maximum number of cached items
            cache_dir: Directory for persistent cache (None for temp)
        """
        self.max_size = max_size
        self.cache_dir = Path(cache_dir) if cache_dir else Path(tempfile.gettempdir()) / "mcp_audio_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._memory_cache = {}
        self._access_times = {}
        self._file_hashes = {}
        self._lock = threading.RLock()
    
    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file for change detection."""
        try:
            stat = os.stat(file_path)
            # Combine file size, modification time, and path
            hash_input = f"{file_path}_{stat.st_size}_{stat.st_mtime}"
            return hashlib.md5(hash_input.encode()).hexdigest()
        except Exception as e:
            logger.warning(f"Failed to get file hash for {file_path}: {e}")
            return str(time.time())  # Fallback to current time
    
    def _get_cache_key(self, file_path: str, operation: str, **kwargs) -> str:
        """Generate cache key for operation."""
        # Include relevant parameters in cache key
        key_data = f"{file_path}_{operation}_{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _cleanup_old_entries(self):
        """Remove oldest entries if cache is full."""
        if len(self._memory_cache) >= self.max_size:
            # Remove 20% of oldest entries
            items_to_remove = max(1, len(self._memory_cache) // 5)
            oldest_keys = sorted(
                self._access_times.keys(),
                key=lambda k: self._access_times[k]
            )[:items_to_remove]
            
            for key in oldest_keys:
                self._memory_cache.pop(key, None)
                self._access_times.pop(key, None)
                
                # Remove from disk cache too
                cache_file = self.cache_dir / f"{key}.pkl"
                if cache_file.exists():
                    try:
                        cache_file.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to remove cache file {cache_file}: {e}")
    
    async def get(self, file_path: str, operation: str, **kwargs) -> Optional[Any]:
        """Get cached result if available and valid."""
        try:
            cache_key = self._get_cache_key(file_path, operation, **kwargs)
            current_hash = self._get_file_hash(file_path)
            
            with self._lock:
                # Check memory cache first
                if cache_key in self._memory_cache:
                    cached_hash, result = self._memory_cache[cache_key]
                    if cached_hash == current_hash:
                        self._access_times[cache_key] = time.time()
                        logger.debug(f"Cache hit (memory): {operation} for {Path(file_path).name}")
                        return result
                    else:
                        # File changed, remove from cache
                        self._memory_cache.pop(cache_key, None)
                        self._access_times.pop(cache_key, None)
                
                # Check disk cache
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                if cache_file.exists():
                    try:
                        with open(cache_file, 'rb') as f:
                            cached_hash, result = pickle.load(f)
                        
                        if cached_hash == current_hash:
                            # Load into memory cache
                            self._memory_cache[cache_key] = (cached_hash, result)
                            self._access_times[cache_key] = time.time()
                            logger.debug(f"Cache hit (disk): {operation} for {Path(file_path).name}")
                            return result
                        else:
                            # File changed, remove from disk
                            cache_file.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to load cache file {cache_file}: {e}")
                        if cache_file.exists():
                            cache_file.unlink()
            
            return None
            
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")
            return None
    
    async def set(self, file_path: str, operation: str, result: Any, **kwargs):
        """Cache result for future use."""
        try:
            cache_key = self._get_cache_key(file_path, operation, **kwargs)
            current_hash = self._get_file_hash(file_path)
            
            with self._lock:
                # Cleanup if necessary
                self._cleanup_old_entries()
                
                # Store in memory cache
                self._memory_cache[cache_key] = (current_hash, result)
                self._access_times[cache_key] = time.time()
                
                # Store in disk cache asynchronously
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                
                def save_to_disk():
                    try:
                        with open(cache_file, 'wb') as f:
                            pickle.dump((current_hash, result), f)
                    except Exception as e:
                        logger.warning(f"Failed to save cache file {cache_file}: {e}")
                
                # Run disk save in thread pool
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, save_to_disk)
                
                logger.debug(f"Cached: {operation} for {Path(file_path).name}")
            
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")
    
    def clear(self):
        """Clear all cached data."""
        with self._lock:
            self._memory_cache.clear()
            self._access_times.clear()
            self._file_hashes.clear()
            
            # Clear disk cache
            try:
                for cache_file in self.cache_dir.glob("*.pkl"):
                    cache_file.unlink()
            except Exception as e:
                logger.warning(f"Failed to clear disk cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            disk_files = len(list(self.cache_dir.glob("*.pkl")))
            return {
                "memory_entries": len(self._memory_cache),
                "disk_entries": disk_files,
                "max_size": self.max_size,
                "cache_dir": str(self.cache_dir)
            }

class PerformanceOptimizer:
    """Performance optimization utilities for audio processing."""
    
    def __init__(self, max_workers: int = None, enable_cache: bool = True):
        """
        Initialize performance optimizer.
        
        Args:
            max_workers: Maximum number of worker threads
            enable_cache: Whether to enable caching
        """
        self.max_workers = max_workers or min(4, (os.cpu_count() or 1) + 1)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.enable_cache = enable_cache
        self.cache = AudioCache() if enable_cache else None
        
        # Performance metrics
        self._operation_times = {}
        self._cache_hits = 0
        self._cache_misses = 0
    
    async def run_with_cache(
        self, 
        operation: str,
        func: Callable,
        file_path: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Run function with caching if enabled.
        
        Args:
            operation: Name of the operation for caching
            func: Function to run
            file_path: Path to audio file
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        start_time = time.time()
        
        try:
            # Try cache first
            if self.enable_cache and self.cache:
                cached_result = await self.cache.get(file_path, operation, **kwargs)
                if cached_result is not None:
                    self._cache_hits += 1
                    return cached_result
                else:
                    self._cache_misses += 1
            
            # Run function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(self.thread_pool, func, *args, **kwargs)
            
            # Cache result
            if self.enable_cache and self.cache and "error" not in result:
                await self.cache.set(file_path, operation, result, **kwargs)
            
            return result
            
        finally:
            # Record performance metrics
            execution_time = time.time() - start_time
            if operation not in self._operation_times:
                self._operation_times[operation] = []
            self._operation_times[operation].append(execution_time)
    
    async def run_parallel(
        self,
        tasks: List[Tuple[str, Callable, tuple, dict]]
    ) -> List[Any]:
        """
        Run multiple tasks in parallel.
        
        Args:
            tasks: List of (name, function, args, kwargs) tuples
            
        Returns:
            List of results in same order as tasks
        """
        async def run_task(name, func, args, kwargs):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(self.thread_pool, func, *args, **kwargs)
            except Exception as e:
                logger.error(f"Task {name} failed: {e}")
                return {"error": f"Task {name} failed: {str(e)}"}
        
        # Run all tasks concurrently
        tasks_to_run = [
            run_task(name, func, args, kwargs)
            for name, func, args, kwargs in tasks
        ]
        
        results = await asyncio.gather(*tasks_to_run, return_exceptions=True)
        
        # Convert exceptions to error dictionaries
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "error": f"Task {tasks[i][0]} failed: {str(result)}"
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def batch_process(self, items: List[Any], batch_size: int = 10) -> List[List[Any]]:
        """
        Split items into batches for processing.
        
        Args:
            items: Items to batch
            batch_size: Size of each batch
            
        Returns:
            List of batches
        """
        batches = []
        for i in range(0, len(items), batch_size):
            batches.append(items[i:i + batch_size])
        return batches
    
    @lru_cache(maxsize=128)
    def get_optimal_chunk_size(self, file_size: int, operation_type: str) -> int:
        """
        Get optimal chunk size for processing based on file size and operation.
        
        Args:
            file_size: Size of audio file in bytes
            operation_type: Type of operation ('analysis', 'separation', 'visualization')
            
        Returns:
            Optimal chunk size
        """
        # Base chunk sizes (in samples)
        base_chunks = {
            'analysis': 22050 * 10,      # 10 seconds at 22050 Hz
            'separation': 22050 * 30,     # 30 seconds for separation
            'visualization': 22050 * 5    # 5 seconds for visualization
        }
        
        base_chunk = base_chunks.get(operation_type, 22050 * 10)
        
        # Adjust based on file size
        if file_size < 1024 * 1024:  # < 1MB
            return base_chunk // 2
        elif file_size > 50 * 1024 * 1024:  # > 50MB
            return base_chunk * 2
        else:
            return base_chunk
    
    def memory_efficient_processing(
        self, 
        data: np.ndarray, 
        process_func: Callable,
        chunk_size: int = None,
        overlap: int = 0
    ):
        """
        Process large arrays in chunks to save memory.
        
        Args:
            data: Input array
            process_func: Function to apply to each chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Yields:
            Processed chunks
        """
        if chunk_size is None:
            chunk_size = min(len(data), 22050 * 10)  # Default 10 seconds
        
        for i in range(0, len(data), chunk_size - overlap):
            end_idx = min(i + chunk_size, len(data))
            chunk = data[i:end_idx]
            
            try:
                result = process_func(chunk)
                yield result
            except Exception as e:
                logger.warning(f"Chunk processing failed at index {i}: {e}")
                continue
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        stats = {
            "thread_pool_workers": self.max_workers,
            "cache_enabled": self.enable_cache,
            "cache_hit_rate": 0.0,
            "operation_performance": {}
        }
        
        # Cache statistics
        if self.enable_cache and self.cache:
            total_requests = self._cache_hits + self._cache_misses
            if total_requests > 0:
                stats["cache_hit_rate"] = self._cache_hits / total_requests
            stats["cache_stats"] = self.cache.get_stats()
        
        # Operation performance
        for operation, times in self._operation_times.items():
            if times:
                stats["operation_performance"][operation] = {
                    "avg_time": np.mean(times),
                    "min_time": np.min(times),
                    "max_time": np.max(times),
                    "total_runs": len(times)
                }
        
        return stats
    
    def clear_cache(self):
        """Clear all cached data."""
        if self.cache:
            self.cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'thread_pool'):
            self.thread_pool.shutdown(wait=False)

# Decorator for automatic caching and performance optimization
def optimize_audio_processing(operation_name: str, use_cache: bool = True):
    """
    Decorator to automatically optimize audio processing functions.
    
    Args:
        operation_name: Name of the operation for caching
        use_cache: Whether to use caching
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to find file_path in arguments
            file_path = None
            if args and isinstance(args[0], str) and Path(args[0]).exists():
                file_path = args[0]
            elif 'file_path' in kwargs:
                file_path = kwargs['file_path']
            
            if file_path and use_cache:
                # Use global optimizer if available
                if hasattr(wrapper, '_optimizer'):
                    optimizer = wrapper._optimizer
                else:
                    optimizer = PerformanceOptimizer()
                    wrapper._optimizer = optimizer
                
                return await optimizer.run_with_cache(
                    operation_name, func, file_path, *args, **kwargs
                )
            else:
                # Run normally
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator