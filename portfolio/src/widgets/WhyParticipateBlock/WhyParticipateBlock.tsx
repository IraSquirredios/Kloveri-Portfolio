import Card from '../../shared/UI/Card/Card'

const WhyParticipateBlock = () => {
    return (
        <div className="mb-10">
            <div className="text-[52px] mb-14 font-medium">
                Зачем участвовать?
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-11">
                <Card className="bg-[url('widgets/WhyParticipateBlock/assets/experience.png')] h-[394px] rounded-[35px] bg-no-repeat bg-right-bottom bg-[length:300px]">
                    <div className="text-[32px] mb-1">Опыт</div>
                    <div className="text-base">
                        Получение опыта работы над реальным командным проектом
                        по современным методологиям разработки
                    </div>
                </Card>
                <Card className="bg-[url('widgets/WhyParticipateBlock/assets/portfolio.png')] h-[394px] rounded-[35px] bg-no-repeat bg-right-bottom bg-[length:401px]">
                    <div className="text-[32px] mb-1">Работа в портфолио</div>
                    <div className="text-base">
                        Получите возможность добавить в портфолио реальный
                        проект
                    </div>
                </Card>
                <Card className="bg-[url('widgets/WhyParticipateBlock/assets/cooperation.png')] h-[394px] rounded-[35px] bg-no-repeat bg-right-bottom bg-[length:378px]">
                    <div className="text-[32px] mb-1">Сотрудничество</div>
                    <div className="text-base">
                        Возможна постоянная работа в команде по развитию сервиса
                        после успешной проверки финансовых гипотез
                    </div>
                </Card>
                <Card className="bg-[url('widgets/WhyParticipateBlock/assets/growth.png')] h-[394px] rounded-[35px] bg-no-repeat bg-right-bottom bg-[length:303px]">
                    <div className="text-[32px] mb-1">Развитие</div>
                    <div className="text-base">
                        Возможное расширение проекта на другие мобильные
                        операционные системы для получения дополнительного опыта
                    </div>
                </Card>
            </div>
        </div>
    )
}

export default WhyParticipateBlock
