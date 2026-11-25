import { InputHTMLAttributes, ReactNode } from 'react'
import { FieldValues, Path, RegisterOptions, UseFormRegister } from 'react-hook-form'

interface InputProps<T extends FieldValues>
    extends InputHTMLAttributes<HTMLInputElement> {
    name: Path<T>
    register: UseFormRegister<T>
    className?: string
    label?: string | ReactNode
    validation?: RegisterOptions<T, Path<T>>
}

export const Input = <T extends FieldValues>(props: InputProps<T>) => {
    const { className, register, name, label, ...rest } = props

    return (
        <div className={['relative mb-3', className].filter(Boolean).join(' ')}>
            {label && <label htmlFor={name}>{label}</label>}
            <input
                className={
                    'peer m-0 block h-[58px] w-full rounded border border-solid border-neutral-300 bg-transparent bg-clip-padding px-3 py-4 text-base font-normal leading-tight text-neutral-700 transition duration-200 ease-linear placeholder:text-transparent focus:border-primary focus:pb-[0.625rem] focus:pt-[1.625rem] focus:text-neutral-700 focus:outline-none peer-focus:text-primary dark:border-neutral-600 dark:text-neutral-200 dark:focus:border-primary dark:peer-focus:text-primary [&:not(:placeholder-shown)]:pb-[0.625rem] [&:not(:placeholder-shown)]:pt-[1.625rem]'
                }
                {...register(name)}
                {...rest}
            />
        </div>
    )
}
