import {http} from '@/utils';
import type {TypeFriendLink} from '@/types/apis/typeFriendLink'

type return_type = {
    status: number
    message: string
}



async function getFriendLink(): Promise<TypeFriendLink[]> {
    return await http.get(`/friend-links`);
}


type TypeFriendLinkStatement = {
    title: string,
    data: string[],
    format: TypeFriendLink,
    questionnaire: string
}

async function getFriendLinkStatements(): Promise<TypeFriendLinkStatement> {
    return await http.get(`/friend-links/statements`);
}


export {
    getFriendLinkCreate,
    getFriendLink,
    getFriendLinkStatements
}