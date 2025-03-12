import {http} from '@/utils';
import type {TypeApiLists} from '@/types/apis/typeApiList'

async function getList(): Promise<TypeApiLists> {
    return await http.get(`/api-list`);
}

export default getList;