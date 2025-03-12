import React from 'react';
import {Input} from 'antd';
import type { GetProps } from 'antd';

type SearchProps = GetProps<typeof Input.Search>;


const SearchComponent: React.FC<SearchProps> = ({onSearch}) => {
    return (
        <Input.Search
            placeholder="输入搜索文本"
            allowClear
            enterButton="搜索"
            size="large"
            onSearch={(value) => {
                if (onSearch) {
                    onSearch(value);
                }
            }}
        />

    );
};

export default SearchComponent;
