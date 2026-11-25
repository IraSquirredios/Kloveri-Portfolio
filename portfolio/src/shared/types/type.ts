export interface ServerResponse<T> {
    status: 'success' | 'error'
    data?: T
    message?: ServerError[] | string
}

export interface ServerError {
    loc: string
    msg: string
}
