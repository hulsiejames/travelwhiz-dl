@echo off
setlocal
pushd "%~dp0"
if not defined SPHINXBUILD set "SPHINXBUILD=sphinx-build"
set "DOC_TARGET=%~1"
if not defined DOC_TARGET set "DOC_TARGET=help"
%SPHINXBUILD% -M %DOC_TARGET% source build %SPHINXOPTS% %O%
set "DOC_RESULT=%ERRORLEVEL%"
popd
exit /b %DOC_RESULT%
