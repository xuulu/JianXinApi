import React from 'react';
import {Empty, Skeleton, Typography} from 'antd';
import getWebsiteStatement from '@/apis/getWebsiteStatement'
import {useRequest} from "ahooks";


const WebsiteStatement: React.FC = () => {
    console.log('WebsiteStatement')
    const {data,loading, error} = useRequest(getWebsiteStatement, {
        cacheKey: `WebsiteStatement`,
        cacheTime: 1000 * 60 * 60 * 24*7,     // 缓存7天
    })

    if (loading || !data) return <Skeleton/>
    if (data == null || data == undefined || error) return <Empty description="获取网站声明数据失败！！"/>
    console.log(data)
    return (
        <Typography className="content">
            <Typography.Title level={2} >{data.title}</Typography.Title>
            {data.data.map(item => <Typography.Paragraph key={item}>{item}</Typography.Paragraph>)}
        </Typography>
    )
}



export default WebsiteStatement