

export interface TypeFriendLink{
    id?: number,
    name: string,
    url: string,
    email: string,
    icon: string,
    description: string | undefined,
}


export interface TypeFriendLinkCreate{
    status: number,
    message: string
}

