import {http} from '@/utils';
import type {TypeApiLists} from '@/types/apis/typeApiList'

async function getSearch(msg: string): Promise<TypeApiLists> {
    return await http.get(`/api-list/search?q=${msg}`);
}

export default getSearch;