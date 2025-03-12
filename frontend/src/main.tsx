import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.tsx'
import './main.module.scss' // 引入全局css


createRoot(document.getElementById('root')!).render(
        <StrictMode>
            <App />
        </StrictMode>
)


