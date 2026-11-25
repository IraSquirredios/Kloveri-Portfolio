import cls from './Modal.module.css'
import { ReactNode } from 'react'

interface ModalProps {
    className?: string
    title?: string | ReactNode
    children: ReactNode
    isOpen: boolean
    onClose?: () => void
}

export const Modal = (props: ModalProps) => {
    const { className, children, title, isOpen, onClose } = props

    return (
        <div
            className={[cls.Modal, isOpen && cls.opened, className]
                .filter(Boolean)
                .join(' ')}
            onClick={onClose}
        >
            <div className={cls.overlay}>
                <div
                    className={cls.content}
                    onClick={(e) => {
                        e.stopPropagation()
                    }}
                >
                    {title && <div className={cls.title}>{title}</div>}
                    {children}
                </div>
            </div>
        </div>
    )
}
