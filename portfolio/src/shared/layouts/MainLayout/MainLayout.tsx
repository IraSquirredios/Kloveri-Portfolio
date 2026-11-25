import { ReactElement, memo } from 'react'
import cls from './MainLayout.module.css'

interface MainLayoutProps {
    header: ReactElement
    content: ReactElement
    footer: ReactElement
}

export const MainLayout = memo((props: MainLayoutProps) => {
    const { content, header, footer } = props

    return (
        <div className={cls.MainLayout}>
            <div className={cls.header}>{header}</div>
            <div className={cls.content}>{content}</div>
            <div className={cls.footer}>{footer}</div>
        </div>
    )
})
