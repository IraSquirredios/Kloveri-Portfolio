import { Link } from 'react-router-dom'
import Card from '../../../../shared/UI/Card/Card'
import { Project } from '../../model/types/project'
import { useMemo } from 'react'

interface ProjectItemProps {
    item: Project
}

const ProjectItem = (props: ProjectItemProps) => {
    const { item } = props

    const currentStep = useMemo(() => ((): Project | undefined => {
        let current
        const steps = item.steps

        steps?.sort((a, b) => {
                return new Date(a.start).getTime() - new Date(b.start).getTime()
            })
            .forEach((step) => {
                if (new Date().getTime() >= new Date(step.start).getTime()) {
                    current = step
                }
            })
        return current
    })(), [item])

    return (
        <Link to={`/projects/${item.id}`}>
            <Card className="hover:shadow-cardShadowHover min-h-[226px] justify-between">
                <div>
                    <div className="text-medium text-[32px] mb-2">
                        {item.title}
                    </div>
                    <div className="text-text-secondary text-base font-normal">
                        {item.description_short}
                    </div>
                </div>
                {currentStep && (
                    <div className="text-accent text-base font-semibold mt-5 after:content-['\00a0→'] after:font-['Arial'] after:ml-0.5">
                        {currentStep.title}
                    </div>
                )}
            </Card>
        </Link>
    )
}

export default ProjectItem
