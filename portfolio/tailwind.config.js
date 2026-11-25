/** @type {import('tailwindcss').Config} */

// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const defaultTheme = require('tailwindcss/defaultTheme')

export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        container: {
            screens: {
                sm: '600px',
                md: '728px',
                lg: '984px',
                xl: '1160px',
                '2xl': '1160px',
            },
        },
        extend: {
            colors: {
                accent: '#2e3192',
                'card-bg': 'rgb(243, 246, 249)',
                'text-secondary': '#787878',
                'link-yellow': '#F0D031',
                'black-custom': '#1f1f1f',
            },
            fontFamily: {
                sans: ['Raleway', ...defaultTheme.fontFamily.sans],
            },
            boxShadow: {
                cardShadow: '0 0 0 0 rgba(0, 0, 0, 0.1)',
                cardShadowHover: '0 0 15px 0 rgba(0, 0, 0, 0.1)',
            },
            backgroundImage: {
                'purple-pattern': "url('/src/shared/assets/noroot.png')",
            },
        },
    },
    plugins: [],
}
