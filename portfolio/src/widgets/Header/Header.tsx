import { Link } from 'react-router-dom'
import Logo from '../../shared/assets/logo.png'
import Button from '../../shared/UI/Button/Button'

const Header = () => {
    return (
        <div className="container mx-auto md:min-h-[var(--header-height)] flex items-center justify-between md:flex-row flex-col md:mb-0 mb-5">
            <Link
                to="/"
                className="cursor-pointer"
            >
                <img
                    src={Logo}
                    alt="logo"
                />
            </Link>
            <div>
                <Button
                    onClick={() =>
                        window.open('https://t.me/cloveri_start_chat', '_blank')
                    }
                    className="font-light px-12 py-3.5"
                >
                    Задать вопрос
                </Button>
            </div>
        </div>
    )
}

export default Header
