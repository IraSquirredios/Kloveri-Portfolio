export type IconName = 'grid' | 'heart' | 'folder' | 'bell' | 'settings' | 'logout' | 'sigma' | 'lace' | 'star' | 'bolt' | 'medical' | 'school' | 'food' | 'wallet';
export type Category = { id: string; name: string };
export type Product = { id?: string; product_name: string; published?: boolean; description: string; status: string; icon: IconName; categoryIds: string[] };
export const demoCategories: Category[] = [
 { id: 'it', name: 'IT' }, { id: 'hr', name: 'HR' },
 { id: 'medicine', name: 'Медицина' }, { id: 'education', name: 'Образование' },
];
// Демонстрационные категории продуктов; заменить данными API при подключении.
export const demoProducts: Product[] = [
 { product_name: 'Сигма', description: 'Аналитическая HR-платформа', status: 'Реализация', categoryIds: ['hr'], icon: 'sigma' },
 { product_name: 'Кружева', description: 'Платформа для управления контактами, бизнес-связями и проектами', status: 'Реализован', categoryIds: ['it'], icon: 'lace' },
 { product_name: 'Кловери', description: 'Экосистема развития IT специалистов', status: 'Остановлен', categoryIds: ['it'], icon: 'star' },
 { product_name: 'Тренды', description: 'Анализ источников, выделение трендов и генерация контента', status: 'Реализован', categoryIds: ['it'], icon: 'bolt' },
 { product_name: 'Майбо', description: 'Медицинская экосистема', status: 'Реализация', categoryIds: ['medicine'], icon: 'medical' },
 { product_name: 'ClassHub', description: 'Образовательная платформа для студентов, преподавателей и работодателей', status: 'Реализация', categoryIds: ['education'], icon: 'school' },
 { product_name: 'OmniNotice', description: 'Платформа для создания продающих рассылок с помощью шаблонов и ИИ', status: 'Реализация', categoryIds: ['it'], icon: 'bell' },
 { product_name: 'Ресторатика', description: 'Платформа персонализированного сервиса для ресторанов', status: 'Реализация', categoryIds: ['it'], icon: 'food' },
 { product_name: 'Цены в магазинах', description: 'Приложение для статистики по изменению цен', status: 'Реализация', categoryIds: ['it'], icon: 'wallet' },
];
