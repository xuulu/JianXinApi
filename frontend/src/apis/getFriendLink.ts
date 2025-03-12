import {http} from '@/utils';
import type {TypeFriendLink} from '@/types/apis/typeFriendLink'

type return_type = {
    status: number
    message: string
}

async function getFriendLinkCreate(data: TypeFriendLink): Promise<return_type> {
    try {
        const response = await http.post(`/friend-links`, data);
        if (response.status === 409) return {status: 409, message: '已成功提交申请，请等待管理员审核！！'};
        if (response.status === 201) return {status: 201, message: '申请成功，请等待管理员审核！！'};
        return {status: 200, message: '提交未知是否成功，请自行检查！！'}
    } catch (error:any) {
        switch (error.response.status) {
            case 201:
                return {
                    status: 201,
                    message: '申请成功，请等待管理员审核！！'
                };
            case 400:
                return {
                    status: 400,
                    message: '请求的参数错误'
                };
            case 409:
                return {
                    status: 409,
                    message: '已成功提交申请，请等待管理员审核！！'
                };
            default:
                return {
                    status: 500,
                    message: '未知错误'
                };
        }

    }
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