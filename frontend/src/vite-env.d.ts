/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly QVQA_ORIGINS: string


  // 更多环境变量...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}


