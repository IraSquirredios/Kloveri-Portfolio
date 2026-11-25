import { useForm, SubmitHandler } from 'react-hook-form'
import { Input } from '../../shared/UI/Input/Input'
import Button from '../../shared/UI/Button/Button'

type ContactFormFields = {
    email: string
    fio: string
    job: string
}

const ContactForm = () => {
    const {
        register,
        handleSubmit,
        // formState: { errors },
    } = useForm<ContactFormFields>()

    const onSubmit: SubmitHandler<ContactFormFields> = (data) =>
        console.log(data)

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Input
                name="email"
                register={register}
                label="Ваш адрес электронной почты"
                validation={{ required: true }}
            />
            <Input
                name="fio"
                register={register}
                label="Имя и фамилия"
            />
            <Input
                name="job"
                register={register}
                label={
                    <div>
                        <strong>Ваша специализация</strong> Вы менеджер?
                        Программист? Тестировщик?
                    </div>
                }
            />
            {/* {errors.fio && <span>This field is required</span>} */}

            <Button type="submit">Отправить</Button>
        </form>
    )
}

export default ContactForm
