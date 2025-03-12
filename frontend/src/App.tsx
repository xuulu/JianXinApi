import {lazy, Suspense} from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {Spin} from 'antd';

const Into = lazy(() => import('@/pages/Into'));
const Layout = lazy(() => import('@/pages/home/layout/Layout'));
const Home = lazy(() => import('@/pages/home'));
const Doc = lazy(() => import('@/pages/home/Doc'));
const FriendLinks = lazy(() => import('@/pages/FriendLinks'));
const WebsiteStatement = lazy(() => import('@/pages/WebsiteStatement'));

const App404 = lazy(() => import('@/pages/error/404'));



const App = () => {
    return (
        <BrowserRouter>
            <Suspense fallback={<Spin fullscreen />}>
                <Routes>
                    <Route path="/" element={<Into/>}/>
                    <Route path="/index" element={<Layout/>}>
                        <Route index element={<Home/>}/>
                        <Route path="doc/:id" element={<Doc />}/>
                        <Route path="friendshiplink" element={<FriendLinks/>}/>
                        <Route path="website-statement" element={<WebsiteStatement/>}/>



                    </Route>

                    {/* 泛型路由，用于处理未找到的页面 */}
                    <Route path="*" element={<App404 />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
};

export default App;
