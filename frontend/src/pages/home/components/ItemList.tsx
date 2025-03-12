import { Card, List } from 'antd';
import { ApiTwoTone,PushpinTwoTone } from '@ant-design/icons';
import {useNavigate} from "react-router-dom";

import type { TypeApiList } from "@/types/apis/typeApiList.ts";

type Props = {
    items: TypeApiList[];
}

const ItemList: React.FC<Props> = ({ items, }) => {
    const navigate = useNavigate()
    return (
        <List
            grid={{
                gutter: 16,
                xs: 1,
                sm: 1,
                md: 1,
                lg: 4,
                xl: 4,
                xxl: 4,
            }}
            dataSource={items}
            renderItem={(item: TypeApiList) => (
                <List.Item>
                    <Card
                        key={item.id}
                        title={item.name}
                        extra={<PushpinTwoTone />}
                        hoverable={true}    // 鼠标悬停时浮起
                        onClick={()=>{navigate(`doc/${item.id}`)}}
                    >
                        <ApiTwoTone />&nbsp;{item.introduce}
                    </Card>
                </List.Item>
            )}
        />
    );
}

export default ItemList;
