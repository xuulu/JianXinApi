import {http} from '@/utils';
import {TypeApiList} from '@/types/apis/typeApiList'

async function getQueryList(id: number | string): Promise<TypeApiList> {
    return await http.get(`/api-list/${id}`);
}

export default getQueryList;