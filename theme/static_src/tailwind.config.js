/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

const pluginCSS = require('tailwindcss/plugin')

const getSizes = (totalSizes = 900, startingValue = 0) => {
    // The following generates an array of increasing values from the totalSizes above.
    const sizeArray = Array.from(Array(startingValue + totalSizes + 1).keys())
    const sliced = sizeArray.slice(startingValue, sizeArray.length)
    
    // Traverse the array and generate sizes in pxs.
    const sizes = sliced.map((i, x) =>
        x > 0 ? { [`${x}`]: `${x}px` } : { [`${x}`]: `${x}px` }
    )

    // Merge the array of objects into a single one
    const sizeObj = Object.assign.apply(Object, sizes)

    return sizeObj
}

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        fontFamily: {
		    sans: ['"Montserrat"', "Arial", "sans-serif"],
		},
        extend: {
            colors: {
                background: '#EFEEE5',
                tickettag: '#68CCF1',
                addcart: '#F18768',
                seecart: '#ED9945',
                shadow: '#1B1702',
                footer: '#151515',
                buy: '#08B936',
                danger: '#CC0000'
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        pluginCSS.withOptions(
            function (options) {
                return function ({ addUtilities, e, variants, theme }) {
                    // ...
                }
            },
            function (options) {
                return {
                    theme: {
						fontSize: {
							11: ['11px', { lineHeight: '13px' }],
							12: ['12px', { lineHeight: '14px' }],
							14: ['14px', { lineHeight: '17px' }],
							16: ['16px', { lineHeight: '19px' }],
							18: ['18px', { lineHeight: '22px' }],
							20: ['20px', { lineHeight: '24px' }],
							24: ['24px', { lineHeight: '29px' }],
							28: ['28px', { lineHeight: '34px' }],
							32: ['32px', { lineHeight: '38px' }],
							30: ['30px', { lineHeight: '36px' }],
							35: ['35px', { lineHeight: '42px' }],
							40: ['40px', { lineHeight: '48px' }],
							46: ['46px', { lineHeight: '55px' }],
							48: ['48px', { lineHeight: '58px' }],
							50: ['50px', { lineHeight: '60px' }],
							52: ['52px', { lineHeight: '62px' }],
							60: ['60px', { lineHeight: '72px' }],
							64: ['64px', { lineHeight: '77px' }],
							72: ['72px', { lineHeight: '86px' }],
							80: ['80px', { lineHeight: '96px' }],
							85: ['85px', { lineHeight: '102px' }],
							90: ['90px', { lineHeight: '108px' }],
                            100: ['100px', { lineHeight: '120px' }],
                            125: ['125px', { lineHeight: '150px' }],
                            128: ['128px', { lineHeight: '153px' }],
                            150: ['150px', { lineHeight: '180px' }],
						},
                        extend: {
                            width: {
                                ...getSizes(1920, 0)
                            },
                            height: {
                                ...getSizes(1920, 0)
                            },
                            minWidth: {
                                ...getSizes(1920, 0)
                            },
                            maxWidth: {
                                ...getSizes(1920, 0)
                            },
                            minHeight: {
                                ...getSizes(1920, 0)
                            },
                            maxHeight: {
                                ...getSizes(1920, 0)
                            },
                            margin: {
                                ...getSizes(1920, 0)
                            },
                            padding: {
                                ...getSizes(1920, 0)
                            },
                            inset: {
                                ...getSizes(1920, 0)
                            },
                            borderWidth: {
                                ...getSizes(100, 0)
                            },
                            spacing: {
                                ...getSizes(200, 0)
                            },
                            size: {
                                ...getSizes(1920, 0)
                            },
                            icon: {
                                ...getSizes(1920, 0)
                            },
                            borderRadius: {
                                ...getSizes(200, 0)
                            },
                            blur: {
                                ...getSizes(300, 0)
                            },
                            backdropBlur: {
                                ...getSizes(300, 0)
                            },
                            left: {
                                ...getSizes(1080, 0)
                            },
                            backgroundSize: {
                                'size-200': '200% 200%',
                            },
                            backgroundPosition: {
                                'pos-0': '0% 0%',
                                'pos-100': '100% 100%',
                            },
                        }
                    }
                }
            }
        )
    ],
};
