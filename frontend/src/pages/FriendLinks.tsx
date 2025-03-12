import {
    Skeleton,
    Typography,
    Card,
    Col,
    Row,
    Avatar,
    List,
    Space,
    Button,
    Modal, Alert,
} from 'antd';
import {getFriendLink, getFriendLinkStatements} from '@/apis/getFriendLink'
import {useRequest} from "ahooks";
import {useState} from "react";


const FriendLinksForm = () => {
    // 获取请求数据
    const {data, loading, error} = useRequest(
        getFriendLinkStatements,
        {
            cacheKey: `FriendLinkStatements`,
            cacheTime: 1000 * 60 * 60 * 24,     // 缓存1天
        })
    if (loading || !data) return <Skeleton/>
    if (error) return <Alert message={error?.message} type="error"/>

    return (

        <>
            <p>申请规则：</p>
            <Typography.Paragraph>{data.data.map(item => <Typography.Text type="danger"
                                                                          key={item}>{item}<br/></Typography.Text>)}</Typography.Paragraph>
            <hr/>
            <p>申请格式：</p>
            <Typography.Text type="success">网站名称：{data.format.name}</Typography.Text><br/>
            <Typography.Text type="success">网站地址：{data.format.url}</Typography.Text><br/>
            <Typography.Text type="success">网站图标：{data.format.icon}</Typography.Text><br/>
            <Typography.Text type="success">网站邮箱：{data.format.email}</Typography.Text><br/>
            <Typography.Text type="success">网站简介：{data.format.description}</Typography.Text><br/>
            <hr/>
            <br/>
            <Typography.Text type="danger">申请地址：
                <a href={data.questionnaire} target="_blank" rel="noopener noreferrer">点我跳转</a>
            </Typography.Text>
            <br/>
            <br/>
            <Typography.Text type="secondary">申请前请先查看申请规则，申请后请耐心等待审核。</Typography.Text>
            <br/>
            <Typography.Text type="secondary">申请失败可发送至QQ1634964或其邮箱，申请通过后，会在网站展示。</Typography.Text>
            <br/>
        </>
    )
};


export default function FriendLinks() {

    // 获取请求数据
    const {data, loading, error} = useRequest(getFriendLink)


    const [isModalOpen, setIsModalOpen] = useState(false);

    if (loading || !data) return <Skeleton/>
    if (error) return <Alert message={error?.message} type="error"/>


    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {

        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };


    const items = () => (
        <List
            grid={{
                gutter: 16,
                xs: 10,
                // sm: 10,
                // md: 10,
                // lg: 40,
                // xl: 40,
                // xxl: 40,
            }}
            dataSource={data}
            renderItem={(item) => (
                <List.Item>
                    <Card
                        key={item.id}
                        hoverable
                        style={{width: 400, height: 'auto'}}
                        onClick={() => {
                            window.open(item.url, '_blank');
                        }}
                    >
                        <Row gutter={16}>
                            <Col flex="none">
                                <Avatar size={64} src={item.icon} alt="头像"/>
                            </Col>
                            <Col flex="auto">
                                <Card.Meta title={item.name} description={item.description}/>
                            </Col>
                        </Row>
                    </Card>

                </List.Item>
            )}
        />
    );

    return (

        <Space direction="vertical" size={20}>
            <Typography.Title level={4}>友情链接:</Typography.Title>
            <Button color="primary" variant="filled" onClick={showModal}>申请友链</Button>
            <Modal
                title="申请友链"
                open={isModalOpen}
                onOk={handleOk}
                onCancel={handleCancel}
            >
                <FriendLinksForm/>
            </Modal>


            {items()}
        </Space>


    )
}