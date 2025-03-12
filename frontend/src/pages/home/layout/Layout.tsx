// import {useState} from "react";
import {useNavigate, Outlet} from 'react-router-dom';
import {Layout, Menu} from 'antd';
import type {MenuProps} from 'antd';
import {
    SwapOutlined,
    HomeOutlined,
    LinkOutlined,
    DiscordOutlined,
} from '@ant-design/icons';

import styles from './layout.module.scss'

const items: MenuProps['items'] = [
    {
        key: '/index',
        label: '首页',
        icon: <HomeOutlined/>

    },
    {
        key: '/index/friendshipLink',
        label: '友情链接',
        // disabled: true, // 禁用
        icon: <LinkOutlined/>
    },
    {
        key: '/index/website-statement',
        label: '网站声明',
        icon: <DiscordOutlined/>
    },
    {
        key: "external",
        label: "外部链接",
        children: [
            {
                key: "external-feedback", // 使用字符串常量
                label: <a href="https://wj.qq.com/s2/18786227/3052/" rel="noopener noreferrer"
                          target="_blank" style={{textDecoration: 'none'}}>匿名反馈</a>,
            },
            {
                key: "external-app", // 使用字符串常量
                label: <a href="https://www.123pan.com/s/TiZKVv-G0GN3.html" rel="noopener noreferrer"
                          target="_blank" style={{textDecoration: 'none'}}>本站app</a>,
            }
        ]
    }
]

const Header = () => {
    const navigate = useNavigate()

    return (
        <Layout.Header className={styles.header}>
            <div className={styles.logo} onClick={() => navigate('/index')}>
                简心API
            </div>
            <Menu
                className={styles.menu}
                mode="horizontal"
                defaultSelectedKeys={['1']}
                forceSubMenuRender={true}   // 在子菜单展示之前就渲染进 DOM
                overflowedIndicator={<SwapOutlined/>}    // 自定义展开图标
                items={items}
                onClick={(e) => {
                    if (e.key == 'external-feedback' || e.key == 'external-app') return null
                    navigate(e.key)
                }}
            />

            {/*<Dropdown*/}
            {/*    className={styles.dropdown}*/}
            {/*    trigger={['click']}*/}
            {/*    menu={{items}}*/}
            {/*>*/}
            {/*    <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>*/}
            {/*        菜单 <DownOutlined/>*/}
            {/*    </a>*/}
            {/*</Dropdown>*/}
        </Layout.Header>
    )
}
const Content = () => {
    return (
        <Layout.Content className={styles.content}>
            <Outlet/>
        </Layout.Content>
    )
}
const Footer = () => {
    return (
        <Layout.Footer className={styles.footer}>
            ©{new Date().getFullYear()} Created by 简心API
        </Layout.Footer>
    )
}

// 布局模板
const HomeLayout = () => {

    return (
        <Layout className={styles.layout}>
            <Header/>
            <Content/>
            <Footer/>
        </Layout>
    )
}

export default HomeLayout



