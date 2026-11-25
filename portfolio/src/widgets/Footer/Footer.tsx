import Logo from '../../shared/assets/logo.png'

const Footer = () => {
    return (
        <div className="md:h-[270px] md:px-0 bg-[#eceff2] px-5">
            <div className="container mx-auto flex flex-col justify-between h-full pb-4">
                <div className="flex justify-between md:flex-nowrap flex-wrap">
                    <div className="md:basis-4/12">
                        <img
                            src={Logo}
                            alt="logo"
                        />
                    </div>
                    <div className="pt-9 md:basis-3/12 text-text-secondary text-base flex flex-col w-full">
                        <a
                            href=""
                            className="mb-3"
                        >
                            Проекты
                        </a>
                        <a
                            href=""
                            className="mb-3"
                        >
                            Цифровой паспорт
                        </a>
                        <a
                            href=""
                            className="mb-3"
                        >
                            Личный кабинет
                        </a>
                    </div>
                    <div className="pt-9 md:basis-3/12 text-text-secondary text-base flex flex-col w-full">
                        <a
                            href=""
                            className="mb-3"
                        >
                            Контакты
                        </a>
                        <a
                            href=""
                            className="mb-3"
                        >
                            Статьи
                        </a>
                        <a
                            href=""
                            className="mb-3"
                        >
                            Лицензионное соглашени
                        </a>
                        <a
                            href=""
                            className="mb-3"
                        >
                            Персональные данные
                        </a>
                    </div>
                    <div className="pt-9 md:basis-2/12 text-[22px] text-[#263238] font-medium w-full">
                        ask@cloveri.org
                    </div>
                </div>
                <div className="text-xl text-[#6d7885]">
                    © ООО “Платформа развития”, 2018 - 2023
                </div>
            </div>
        </div>
    )
}

export default Footer
