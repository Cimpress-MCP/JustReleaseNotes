import os

class dll:

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
        verstrings = []
        sigstrings = self.__findsignatures(fn)
        if sigstrings[0] == '':
            return None
        for i in sigstrings:
            FV = self.__normalizer(i.split(',')[8:16])
            FOS = self.__normalizer(i.split(',')[32:36])
            hexver = FV[3]+FV[2]+FV[1]+FV[0]+':'+FV[7]+FV[6]+FV[5]+FV[4]
            if hexver not in verstrings:
               verstrings.append(hexver)
        myver = max(verstrings)
        return self.__parsver(myver)

    def __createparsestruct(self, b):
        s= ''
        for i in range(len(b)):
            byte = b[i]
            if type(byte) is str:
                byte = ord(byte)
            s += hex(byte)+','
        return s[:-1]

    def __findsignatures(self, sz):
        res = []
        indx=sz.find(b'\xbd\x04\xef\xfe')
        cnt = sz.count(b'\xbd\x04\xef\xfe')
        while cnt > 1:
            s = self.__createparsestruct(sz[indx:indx+52])
            sz = sz[indx+1:]
            cnt = sz.count(b'\xbd\x04\xef\xfe')
            indx=sz.find(b'\xbd\x04\xef\xfe')
            res.append(s)
        res.append(self.__createparsestruct(sz[indx:indx+52]))
        return res

    def __parsver(self, v):
        a,b,c,d = v[:4], v[4:8], v[9:13], v[13:]
        return str(int(a,16)) + '.'+ str(int(b,16)) +'.' + str(int(c,16)) + '.' + str(int(d,16))
