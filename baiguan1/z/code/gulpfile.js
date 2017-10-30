var gulp = require('gulp');
var watch = require('gulp-watch');
var spawn = require('child_process').spawn;
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var bower = require('gulp-bower');
var less = require('gulp-less');
var jshint = require('gulp-jshint');

var paths = {
    js: ['frontend/js/**/*.js'],
    dist: ['./frontend/dist/**/*'],
    vendor: ['./vendor/**/dist/**/*'],
    bower: ['./bower.json'],
    less: ['frontend/less/**/*.less'],
    css: ['frontend/css/**/*.css'],
    images: ['frontend/images/**/*.*']
}

gulp.task('less', function() {
    return gulp.src(paths.less)
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('./static/css'))
})

gulp.task('css', function() {
    return gulp.src(paths.css)
        .pipe(gulp.dest('./static/css'))
})

gulp.task('images', function() {
    return gulp.src(paths.images)
        .pipe(gulp.dest('./static/images'))
})

gulp.task('vendor', function () {
    return bower({directory: './static/vendor'})
});

gulp.task('javascript', function() {
    return gulp.src(paths.js)
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('static/js'));
});

gulp.task('build', ['vendor', 'javascript', 'less', 'css', 'images']);

gulp.task('start', function() {
    gulp.watch(paths.js, ['javascript']);
    gulp.watch(paths.bower, ['vendor']);
    gulp.watch(paths.less, ['less']);
    gulp.watch(paths.css, ['css']);
    gulp.watch(paths.images, ['images']);
});

gulp.task('default', ['start', 'build']);
