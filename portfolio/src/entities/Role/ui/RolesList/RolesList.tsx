import Card from '../../../../shared/UI/Card/Card'
import { ProjectRole } from '../../model/types/role'

interface RolesListProps {
    roles: ProjectRole[]
    title: string
}

const RolesList = (props: RolesListProps) => {
    const { roles, title } = props
    const withHttps = (link: string) =>
        !/^https?:\/\//i.test(link) ? `https://${link}` : link

    return (
        <>
            <div className="text-[52px] font-medium mb-14">{title}</div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                {roles.map((role, index) => {
                    const link = role.link && withHttps(role.link)

                    return link ? (
                        <a
                            href={link}
                            target="_blank"
                        >
                            <RoleItem
                                role={role}
                                key={index}
                            />
                        </a>
                    ) : (
                        <RoleItem
                            role={role}
                            key={index}
                        />
                    )
                })}
            </div>
        </>
    )
}

const RoleItem = ({ role }: { role: ProjectRole }) => {
    return (
        <Card className="min-h-[140px] group/roleCard">
            <div className="font-semibold text-xl mb-1">{role.title}</div>
            <div>
                {role.amount +
                    ' ' +
                    (role.amount === 1
                        ? 'место'
                        : role.amount > 1 && role.amount < 5
                        ? 'места'
                        : 'мест')}
                {/* //! */}
            </div>

            {role.link && (
                <div className="invisible group-hover/roleCard:visible text-accent text-base font-semibold mt-5 after:content-['\00a0→'] after:font-['Arial'] after:ml-0.5">
                    Заполнить анкету
                </div>
            )}
        </Card>
    )
}

export default RolesList
