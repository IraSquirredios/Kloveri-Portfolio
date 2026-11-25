import { ButtonHTMLAttributes, ReactNode } from 'react'

type ButtonTheme = 'blue' | 'black'
type ButtonRound = 'none' | 'small' | 'medium' | 'full'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode
    className?: string
    theme?: ButtonTheme
    round?: ButtonRound
}

const mapThemeClass: Record<ButtonTheme, string> = {
    blue: 'ease-out duration-150 bg-accent text-white hover:bg-accent/90',
    black: 'ease-out duration-150 bg-black-custom text-white hover:bg-black-custom/90',
}

const mapRoundClass: Record<ButtonRound, string> = {
    none: '',
    small: 'rounded-lg',
    medium: 'rounded-[35px]',
    full: 'rounded-full'
}

const Button = (props: ButtonProps) => {
    const { children, className, theme = 'blue', round = 'small', ...rest } = props

    return (
        <button
            className={[
                className,
                mapThemeClass[theme],
                mapRoundClass[round],
                'text-sm font-medium',
            ]
                .filter(Boolean)
                .join(' ')}
            {...rest}
        >
            {children}
        </button>
    )
}

export default Button
