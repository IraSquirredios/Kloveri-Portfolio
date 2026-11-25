import { type CSSProperties } from 'react'
import cls from './Skeleton.module.css'

interface SkeletonProps {
    className?: string
    height?: number | string
    width?: number | string
    border?: number | string
}

export const Skeleton = (props: SkeletonProps) => {
    const { className, border, width, height } = props

    const styles: CSSProperties = {
        width,
        height,
        borderRadius: border,
    }

    return (
        <div
            className={[cls.Skeleton, className].filter(Boolean).join(' ')}
            style={styles}
        />
    )
}
