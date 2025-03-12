import {Button, Typography} from "antd";
import {useNavigate} from "react-router-dom"



const {Title, Paragraph} = Typography;
import styles from './home.module.scss';

export default function Home() {
    const navigate = useNavigate()
    return (
        <div className={styles.homeContainer}>
            <Title>简心API</Title>
            <Paragraph>为用户提供安全可靠的接口服务平台</Paragraph>
            <i className="bi-chevron-down btn-lg"></i>
            <Button type='primary' onClick={() => navigate("/index")}>开始使用</Button>
        </div>

    )
}
