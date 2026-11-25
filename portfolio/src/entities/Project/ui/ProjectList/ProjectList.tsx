import ProjectItem from '../ProjectItem/ProjectItem'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { Project } from '../../model/types/project'
import { Skeleton } from '../../../../shared/UI/Skeleton/Skeleton'
import { ServerResponse } from '../../../../shared/types/type'
import { Modal } from '../../../../shared/UI/Modal/Modal'
import ContactForm from '../../../../features/ContactForm/ContactForm'

const ProjectList = () => {
    const [projects, setProjects] = useState<Project[]>([])
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [contactModalisOpen, setContactModalisOpen] = useState(false)

    useEffect(() => {
        const fetchProjects = async () => {
            setIsLoading(true)
            const response = await axios.get<ServerResponse<Project[]>>(
                'https://api.portfolio.skroy.ru/project',
            )

            if (response.data.status === 'success' && response.data.data) {
                const onlyPublished = response.data.data.filter(
                    (el) => el.pub_status !== false,
                )

                setProjects(onlyPublished)
                setTimeout(() => setIsLoading(false), 200)
            }
        }
        fetchProjects()
    }, [])

    if (isLoading) {
        return (
            <div className="mt-[90px] grid md:grid-cols-2 grid-cols-1 gap-10">
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
                <Skeleton
                    height={'226px'}
                    border={'20px'}
                />
            </div>
        )
    }
    if (!projects.length) {
        return null
    }
    return (
        <div className="mt-[90px] grid md:grid-cols-2 grid-cols-1 gap-10">
            {projects.map((project) => (
                <ProjectItem
                    item={project}
                    key={project.id}
                />
            ))}
            <div className="bg-accent rounded-[20px] shadow-cardShadow px-[30px] pt-[30px] pb-[40px] hover:shadow-cardShadowHover min-h-[226px]">
                <div className="text-white text-2xl/[1.55]">
                    <p>Не нашли проект для старта?</p>
                    <p>Пришлем письмо на почту, когда появится новый набор</p>
                </div>
                <div
                    className="text-link-yellow text-base font-semibold mt-5 after:content-['\00a0→'] after:font-['Arial'] after:ml-0.5 hover:underline cursor-pointer"
                    onClick={() => setContactModalisOpen(true)}
                >
                    Оставить контакты
                </div>
            </div>
            <Modal
                onClose={() => setContactModalisOpen(false)}
                isOpen={contactModalisOpen}
                title={
                    <>
                        <div>Хотите на практику?</div>
                        <div>
                            Оставьте контакты, и мы пришлем приглашение на
                            участие в новых проектах
                        </div>
                    </>
                }
            >
                <ContactForm />
            </Modal>
        </div>
    )
}

export default ProjectList
