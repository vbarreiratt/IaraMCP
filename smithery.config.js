// 🧜‍♀️ IaraMCP - Smithery Advanced Configuration
// Configuração avançada para resolver problemas de build e timeout

export default {
  esbuild: {
    // Marcar pacotes problemáticos como externos para evitar bundling issues
    external: [
      // Pacotes de Machine Learning pesados que causam timeouts
      "torch",
      "torchaudio", 
      "demucs",
      "tensorflow",
      "transformers",
      
      // Pacotes nativos de audio que podem causar problemas de build
      "soundfile",
      "librosa",
      "essentia",
      "madmom",
      
      // Core MCP - manter como externo para evitar conflitos
      "fastmcp",
      "mcp",
      
      // Bibliotecas científicas com dependências nativas
      "numpy",
      "scipy",
      "scikit-learn",
      "matplotlib",
      "seaborn"
    ],
    
    // Configurações de otimização para evitar timeouts
    minify: false, // Desabilitar minificação para acelerar build
    sourcemap: false, // Desabilitar sourcemaps para reduzir tamanho
    
    // Target para compatibilidade com container
    target: "node18",
    platform: "node",
    format: "esm"
  }
}