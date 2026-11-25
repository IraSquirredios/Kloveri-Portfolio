import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Project } from '../../entities/Project/model/types/project'
import Card from '../../shared/UI/Card/Card'
import axios from 'axios'
import { Skeleton } from '../../shared/UI/Skeleton/Skeleton'
import WhyParticipateBlock from '../../widgets/WhyParticipateBlock/WhyParticipateBlock'
import RolesList from '../../entities/Role/ui/RolesList/RolesList'
import { HashLink } from 'react-router-hash-link'
import Button from '../../shared/UI/Button/Button'

const ProjectDetailsPage = () => {
    const { id } = useParams()
    const [project, setProject] = useState<Project>({})
    const [isLoading, setIsLoading] = useState<boolean>(false)

    useEffect(() => {
        const fetchProjects = async () => {
            setIsLoading(true)
            const response = await axios.get(
                `https://api.portfolio.skroy.ru/project/${id}`,
            )
            // console.log(response.data.data)
            setProject(response.data.data)
            setIsLoading(false)
        }
        try {
            fetchProjects()
        } catch (e) {
            console.log(e)
        }
    }, [id])

    useEffect(() => {
        window.scroll({ top: 0 })
    }, [])

    if (isLoading) {
        return (
            <>
                <div className="container mx-auto">
                    <div className="h-[80px] flex flex-col md:flex-row items-center gap-7 mb-10">
                        <div className="text-xl font-light">При поддержке</div>
                        <div className="flex gap-3">
                            <Skeleton
                                className="h-7"
                                width={'200px'}
                            />
                        </div>
                    </div>
                </div>
                <div className="lg:px-10">
                    <Skeleton className="w-full h-[400px] rounded-[30px] mb-14" />
                </div>
                <div className="container mx-auto mb-14">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-32">
                        <Skeleton className="flex gap-5 h-[159px] rounded-[20px]" />
                        <Skeleton className="flex gap-5 h-[159px] rounded-[20px]" />
                        <Skeleton className="flex gap-5 h-[159px] rounded-[20px]" />
                    </div>
                </div>
            </>
        )
    }
    if (!id || !project) {
        return <div>Проект удален или не существует</div>
    }
    return (
        <div className="mx-5 md:mx-0">
            {project.partners?.length !== 0 && (
                <div className="container mx-auto">
                    <div className="h-[80px] flex flex-col md:flex-row items-center gap-7 mb-10">
                        <div className="text-xl font-light">При поддержке</div>
                        <div className="flex gap-3">
                            {project.partners?.map((partner) => {
                                return (
                                    <img
                                        src={partner.logo}
                                        alt=""
                                        className="object-contain h-7"
                                        key={partner.logo}
                                    />
                                )
                            })}
                        </div>
                    </div>
                </div>
            )}
            <div className="lg:px-10">
                <div
                    className={[
                        'w-full h-[400px] rounded-[30px] bg-no-repeat bg-cover bg-center mb-14 bg-card-bg',
                        project.logo
                            ? `bg-[image:var(--image-url)]`
                            : 'bg-purple-pattern',
                    ]
                        .filter(Boolean)
                        .join(' ')}
                    style={
                        {
                            '--image-url': `url(${project.logo})`,
                        } as React.CSSProperties
                    }
                >
                    <div className="container flex flex-col justify-center h-full text-white gap-12 pb-10 mx-5 md:mx-auto">
                        {project.title && (
                            <div className="text-6xl font-medium">
                                {project.title}
                            </div>
                        )}
                        {project.description_short && (
                            <div className="text-2xl font-light">
                                {project.description_short}
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <div className="container mx-auto mb-14">
                {project.steps && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-32">
                        {project.steps.map((step) => (
                            <Card
                                className="flex gap-5 h-[159px]"
                                key={step.title}
                            >
                                <div className="text-lg text-accent">
                                    {new Date(step.start).toLocaleString('ru', {
                                        year: 'numeric',
                                        month: 'long',
                                        day: 'numeric',
                                    })}
                                </div>
                                <div className="text-[22px]">{step.title}</div>
                            </Card>
                        ))}
                    </div>
                )}

                {project.description && (
                    <div className="flex pb-32 flex-col md:flex-row">
                        <div className="w-ful md:w-5/12">
                            <div className="text-[52px] font-medium">
                                О проекте
                            </div>
                            {/* <div className="text-text-secondary font-medium">
                                апрель - август 2023
                            </div> */}
                        </div>
                        <div className="w-full md:w-7/12 text-xl font-light">
                            <pre className="font-sans whitespace-pre-wrap">
                                {project.description}
                            </pre>
                        </div>
                    </div>
                )}

                {project.description_extra && (
                    <div className="flex pb-52 flex-col md:flex-row">
                        <div className="w-full md:w-5/12">
                            <div className="text-[52px]/[1.23] font-medium">
                                Как будем работать?
                            </div>
                        </div>
                        <div className="w-full md:w-7/12 text-xl font-light">
                            <pre className="font-sans whitespace-pre-wrap">
                                {project.description_extra}
                            </pre>
                        </div>
                    </div>
                )}

                {project.roles && (
                    <div
                        id={'roles'}
                        className="mb-52"
                    >
                        <RolesList
                            title="Роли в проекте"
                            roles={project.roles}
                        />
                    </div>
                )}

                <WhyParticipateBlock />

                {project.roles && (
                    <HashLink
                        to="#roles"
                        smooth
                    >
                        <Button
                            theme="black"
                            round="medium"
                            className="w-full p-14"
                        >
                            <span className="text-3xl uppercase">
                                Хочу на стажировку
                            </span>
                        </Button>
                    </HashLink>
                )}
            </div>
        </div>
    )
}

export default ProjectDetailsPage
