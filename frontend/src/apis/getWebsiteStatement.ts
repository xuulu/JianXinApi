import {http} from '@/utils';

type types = {
    title: string
    data: string[]
}



async function getList(): Promise<types> {
    return await http.get(`/api-list/website-statements`);
}

export default getList;