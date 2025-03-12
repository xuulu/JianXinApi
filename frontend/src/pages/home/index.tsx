import {useState, useEffect} from "react";
import {useRequest} from 'ahooks'
import type {TypeApiLists} from '@/types/apis/typeApiList'
import getList from "@/apis/getList";
import getSearch from "@/apis/getSearch";
import {Skeleton, Alert, Typography} from "antd";
import ItemList from "./components/ItemList";
import Search from "./components/Search";

import styles from './home.module.scss'


const Home = () => {
    // 数据源
    const [data, setData] = useState<TypeApiLists | undefined>()

    const {data: dataSource, loading, error, run} = useRequest(getList, {
        manual: true,
        cacheKey: `home-index`,
        onSuccess: (response) => {
            setData(response)
        }
    })

    // 首次加载
    useEffect(() => {
        console.log('加载首页数据')
        run()
    }, [])


    if (loading) return <Skeleton active/>
    if (error) return <Alert message={error?.message} type="error"/>
    if (dataSource === null || data === undefined) return <Alert message="数据为空" type="info" closable/>


    // 处理搜索
    const handleSearch = (value: string) => {
        console.log('搜索值:', value);
        getSearch(value).then(res => {
            setData(res)
        })
    };

    return (
        <div className={styles.content}>
            <div className={styles.centered}>
                <Typography.Title level={3}>简 心 A P I</Typography.Title>
                <Typography.Text disabled>一个基于最新技术栈的接口平台，前端使用React+Antd等构建，后端使用Django+drf提供接口服务(现已转向FastAPI)。</Typography.Text>
                <br/>
                <Typography.Text type="secondary" delete>tips：有无<a href={'https://api.qvqa.cn/api/web-api'}target="_blank">前端</a>大佬重写本站UI，联系站长QQ:1634964</Typography.Text>
                <Search onSearch={handleSearch} />
            </div>

            <br></br>

            <ItemList items={data}/>
        </div>
    )

}

export default Home