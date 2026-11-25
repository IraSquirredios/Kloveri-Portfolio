import { ReactNode } from 'react'

interface CardProps {
    children: ReactNode
    className?: string
}

const Card = (props: CardProps) => {
    const { children, className } = props

    return (
        <div
            className={[
                'bg-card-bg rounded-[20px] shadow-cardShadow px-[30px] pt-[30px] pb-[40px] flex flex-col',
                className,
            ]
                .filter(Boolean)
                .join(' ')}
        >
            {children}
        </div>
    )
}

export default Card
