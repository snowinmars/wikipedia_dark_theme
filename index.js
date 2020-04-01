import compileSass from 'compile-sass';
app.use('/css/:cssName', compileSass());
