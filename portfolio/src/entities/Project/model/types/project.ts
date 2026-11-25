import { ProjectRole } from '../../../Role/model/types/role'

export interface Project {
    id?: number
    title?: string
    description?: string
    description_short?: string
    description_extra?: string
    author_id?: number
    logo?: string
    budget?: number
    ts_created?: string
    ts_changed?: string
    ts_published?: string
    pub_status?: boolean
    stage?: ProjectStage
    partners?: ProjectPartner[]
    steps?: ProjectStep[]
    roles?: ProjectRole[]
    // categories?: ProjectCategory[]
    // budget_currency?: Currency
}

export interface ProjectStage {
    id?: number
    title?: string
}

export interface ProjectStep {
    title: string
    start: string
    end?: string
}

export interface ProjectPartner {
    title?: string
    logo: string
}

// export interface Currency {
//     code: string
//     id: number
//     symbol: string
//     title: string
// }

// export interface ProjectCategory {
//     id?: number
//     title?: string
// }
