export type TypeRequestParameters = {
    parameter: string,
    type: string,
    required: boolean,
    description: string
}


export interface TypeApiList {
    "id"?: number,
    "name": string,
    "path": string,
    "type": string[],
    "urlExample"?: string,
    "introduce"?: string,
    "requestParameters"?: TypeRequestParameters[] | null | '' | undefined,
    "returnParameters"?: string,
}

export type TypeApiLists = TypeApiList[]

