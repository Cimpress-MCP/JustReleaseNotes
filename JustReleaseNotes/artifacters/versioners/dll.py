import os

class dll:

    __VOS_DOS             = 0x00010000L
    __VOS_OS216           = 0x00020000L
    __VOS_OS232           = 0x00030000L
    __VOS_NT              = 0x00040000L
    __VOS__BASE           = 0x00000000L
    __VOS__WINDOWS16      = 0x00000001L
    __VOS__PM16           = 0x00000002L
    __VOS__PM32           = 0x00000003L
    __VOS__WINDOWS32      = 0x00000004L
    __VOS_DOS_WINDOWS16   = 0x00010001L
    __VOS_DOS_WINDOWS32   = 0x00010004L
    __VOS_OS216_PM16      = 0x00020002L
    __VOS_OS232_PM32      = 0x00030003L
    __VOS_NT_WINDOWS32    = 0x00040004L

    def extractVersions(self, fileContent, fileName):
        if fileContent is None:
            return None
        dependencyVersion = self.__calcversioninfo(fileContent)
        res = []
        res.append("{0}: {1}".format(os.path.basename(fileName), dependencyVersion))
        return res


    def __normalizer(self, s):
        for j in range(len(s)):
            if len(s[j]) > 3:
                k = s[j][2:]
            else:
                k = '0' + s[j][2:]
            s[j] = k
        return s

    def __calcversioninfo(self, fn):
        ostypes = [self.__VOS_DOS, self.__VOS_NT, self.__VOS__WINDOWS32, self.__VOS_DOS_WINDOWS16,
                   self.__VOS_DOS_WINDOWS32, self.__VOS_NT_WINDOWS32]

        verstrings = []
        sigstrings = self.__findsignatures(fn)
        if sigstrings[0] == '':
            return None
        for i in sigstrings:
            FV = self.__normalizer(i.split(',')[8:16])
            FOS = self.__normalizer(i.split(',')[32:36])
            hexver = FV[3]+FV[2]+FV[1]+FV[0]+':'+FV[7]+FV[6]+FV[5]+FV[4]
            OStag = long('0x' + FOS[3]+FOS[2]+FOS[1]+FOS[0] + 'L',16)
            if OStag not in ostypes:
               continue
            if hexver not in verstrings:
               verstrings.append(hexver)
        myver = max(verstrings)
        return self.__parsver(myver)

    def __createparsestruct(self, b):
        s= ''
        for i in range(len(b)):
            s += hex(ord(b[i]))+','
        return s[:-1]

    def __findsignatures(self, sz):
        res = []
        indx=sz.find('\xbd\x04\xef\xfe')
        cnt = sz.count('\xbd\x04\xef\xfe')
        while cnt > 1:
            s = self.__createparsestruct(sz[indx:indx+52])
            sz = sz[indx+1:]
            cnt = sz.count('\xbd\x04\xef\xfe')
            indx=sz.find('\xbd\x04\xef\xfe')
            res.append(s)
        res.append(self.__createparsestruct(sz[indx:indx+52]))
        return res

    def __parsver(self, v):
        a,b,c,d = v[:4], v[4:8], v[9:13], v[13:]
        return str(int(a,16)) + '.'+ str(int(b,16)) +'.' + str(int(c,16)) + '.' + str(int(d,16))
