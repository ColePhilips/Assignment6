// karma.conf.js
module.exports = function(config) {
    config.set({
        basePath: '', // Base path that will be used to resolve all patterns (e.g. files, exclude)
        frameworks: ['jasmine'], // Testing framework to use
        files: [
            // Load AngularJS and Angular Mocks from CDN
            'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js',
            'https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular-mocks.js',
            // Load your application files
            'public/app.js', // Path to your AngularJS application file
            // Load your test files
            'src/app.test.js' // Path to your test file
        ],
        preprocessors: {
            'public/app.js': ['coverage'] // Preprocess app.js with coverage
        },
        reporters: ['progress', 'coverage'], // Reporters to use
        coverageReporter: {
            type: 'html', // Output format for coverage report
            dir: 'coverage/' // Directory to output coverage reports
        },
        browsers: ['Chrome'], // Browsers to launch for testing
        singleRun: true, // If true, Karma captures browsers, runs the tests, and exits
        concurrency: Infinity, // Concurrency level
        logLevel: config.LOG_INFO, // Log level
        autoWatch: false // Disable auto-watching for changes
    });
};