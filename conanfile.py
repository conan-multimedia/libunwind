from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os

class LibunwindConan(ConanFile):
    name = "libunwind"
    version = "1.2.1"
    description = "The primary goal of this project is to define a portable and efficient"
    "C programming interface (API) to determine the call-chain of a program"
    url = "https://github.com/conan-multimedia/libunwind"
    homepage = "http://www.nongnu.org/libunwind/"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        
        tools.get("https://github.com/{name}/{name}/archive/v{version}.tar.gz".format(name=self.name, version =self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        #copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/aux/config.guess"%(os.getcwd()))
        #copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/aux/config.sub"%(os.getcwd()))
        #copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config/config.guess"%(os.getcwd()))
        #copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config/config.sub"%(os.getcwd()))
        #self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
        #' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        #self.run("make -j4")
        #self.run("make install")

        with tools.chdir(self.source_subfolder):
            self.run('./autogen.sh')
            _args = ["--prefix=%s/builddir"%(os.getcwd()), "--disable-silent-rules", "--enable-introspection"]
            #if self.options.shared:
            #    _args.extend(['--enable-shared=yes','--enable-static=no'])
            #else:
            #    _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                excludes = "*.a" if self.options.shared else "*.so*"
                self.copy("*", src="%s/builddir"%(os.getcwd()), excludes =excludes)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

