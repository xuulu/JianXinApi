import {defineConfig} from 'vite'
import {join} from 'path'
import react from '@vitejs/plugin-react'
import viteCompression from 'vite-plugin-compression2'   // 压缩插件
import ExternalGlobals from 'rollup-plugin-external-globals'
import {visualizer} from 'rollup-plugin-visualizer'


// 根据环境变量选择配置
export default defineConfig(({command}) => {

    // 共同配置
    const commonConfig = {
        plugins: [react()],
        envPrefix: ['QVQA_'], // 自定义环境变量前缀
        resolve: {
            alias: {
                '@': join(__dirname, 'src')
            },
        },
        css: {
            preprocessorOptions: {
                less: {
                    javascriptEnabled: true,
                    modifyVars: {},
                },
            },
        }
    }
    // 开发配置
    const serve = {}

    // 打包配置
    const build = {
        plugins: [
            viteCompression({
                algorithm: 'gzip',
                deleteOriginalAssets: true, // 删除未压缩的文件
                threshold: 10240, // 对超过10KB的文件进行压缩
            }),
        ],
        build: {
            outDir: 'dist',
            minify: 'esbuild' as const,
            // minify: 'terser',    // terser 或 esbuild
            terserOptions: {
                compress: {
                    // 生产环境时移除console.log调试代码
                    drop_console: true,
                    drop_debugger: true,
                }
            },
            rollupOptions: {
                treeshake: true,    // 摇掉无用代码
                external: ['react', 'react-dom', 'axios'],
                plugins: [
                    ExternalGlobals({
                        react: 'React',
                        'react-dom': 'ReactDOM',
                        axios: 'axios'
                    }),
                    visualizer()
                ],

                output: {
                    chunkFileNames: 'js/[name]-[hash].js', // 引入文件名的名称
                    entryFileNames: 'js/[name]-[hash].js', // 包的入口文件名称
                    assetFileNames: '[ext]/[name]-[hash].[ext]', // 资源文件像 字体，图片等


                    manualChunks: (id: string) => {
                        // 这个ID，就是所有文件的绝对路径
                        if (id.includes("node_modules")) {
                            if (id.includes('antd')) return 'antd'

                            // 让每个插件都打包成独立的文件
                            return 'node_modules'
                        }
                    }
                }
            }
        }
    }


    if (command === 'serve') {
        console.log('生产环境')
        return {
            ...commonConfig,
            ...serve
        }
    } else {
        console.log('打包配置')
        return {
            ...commonConfig,
            ...build
        }
    }

});


