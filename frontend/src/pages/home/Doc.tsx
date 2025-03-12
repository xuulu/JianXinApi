import {useEffect} from 'react';
import {Alert, Descriptions, Skeleton, Table, TableProps, Tag, Typography} from "antd";
import {useNavigate, useParams} from "react-router-dom";
import getQueryApi from "@/apis/getQueryApi";
import {useRequest, useTitle} from "ahooks";
import type {TypeRequestParameters} from '@/types/apis/typeApiList'


const Doc: React.FC = () => {
    useTitle(`简心API文档`);
    const {id} = useParams()
    const navigate = useNavigate();

    const {data, loading, error, run} = useRequest(
        () => getQueryApi(id as string),
        {
            cacheKey: `doc-${id}`,
            cacheTime: 1000 * 60 * 60 * 24,     // 缓存1天
            manual: true,                       // 设置为手动触发
        }
    )
    useEffect(() => {
        run(); // 调用 run 方法来执行请求
    }, [id])

    if (loading) return <Skeleton active/>
    if (error) {
        navigate('/index')
        return <Alert message={'获取数据失败！'} type="error"/>
    }
    if (data === null || data === undefined) {
        navigate('/index')
        return <Alert message="数据为空" type="info" closable/>
    }


    // 接口类型
    const apiType = () => {
        // 定义颜色映射
        const tagColorMap: { [key: string]: string } = {
            json: 'cyan',
            image: 'warning',
            video: 'purple',
        };
        return data.type
            .map((item: string, index: number) => {
                const color = tagColorMap[item] || 'default'; // 默认颜色为 'default'
                return <Tag key={index} color={color}>{item}</Tag>;
            });
    };


    // 请求参数
    const requestParameters = () => {
        if (data.requestParameters == '' || data.requestParameters == null || data.requestParameters == undefined) return null
        //  默认数据 type
        const initialSource = [
            {
                parameter: 'type',
                type: 'str',
                required: false,
                description: '全局参数,支持json|image|video等'
            }]

        initialSource.push(...data.requestParameters)

        // 表格配置
        const columns: TableProps<TypeRequestParameters>['columns'] = [
            {
                title: '参数',
                dataIndex: 'parameter',
                key: 'parameter'
            },
            {
                title: '类型',
                dataIndex: 'type',
                key: 'type',
                render: (type: string) => (<Tag color="processing">{type}</Tag>),
            },
            {
                title: '必填',
                dataIndex: 'required',
                key: 'required',
                render: (required: boolean) => (required ? <Tag color="success">是</Tag> : <Tag color="error">否</Tag>),
            },
            {
                title: '描述',
                dataIndex: 'description',
                key: 'description',
            },

        ];
        return (
            <Descriptions.Item label="请求参数">
                <Table
                    bordered={true}
                    columns={columns}
                    dataSource={initialSource}
                    // rowKey="parameter"
                    pagination={false}
                />
            </Descriptions.Item>
        )
    }


    return (

        <Descriptions
            title='&nbsp;&nbsp;&nbsp;接口文档'
            bordered
            column={{xs: 1, sm: 1, md: 1, lg: 1, xl: 1, xxl: 1}}
            layout='vertical'
        >
            <Descriptions.Item label="接口名称">{data.name}</Descriptions.Item>
            <Descriptions.Item label="接口说明">
                <div>{data.introduce}</div>
            </Descriptions.Item>
            <Descriptions.Item label="请求地址">
                {/*添加复制按钮*/}
                <a target="_blank"
                   href={`https://api.qvqa.cn/api/${data.path}`}>
                    <Typography.Paragraph copyable underline>
                        {`https://api.qvqa.cn/api/${data.path}`}
                    </Typography.Paragraph>
                </a>
            </Descriptions.Item>
            <Descriptions.Item label="请求示例">
                <a target="_blank"
                   href={`https://api.qvqa.cn/api/${data.path}/${data.urlExample}`}>
                    <Typography.Paragraph copyable underline>
                        {`https://api.qvqa.cn/api/${data.path}/${data.urlExample}`}
                    </Typography.Paragraph>
                </a>
            </Descriptions.Item>
            <Descriptions.Item label="接口类型">
                {apiType()}
            </Descriptions.Item>
            {/*请求参数函数*/}
            {requestParameters()}

        </Descriptions>
    )
}

export default Doc