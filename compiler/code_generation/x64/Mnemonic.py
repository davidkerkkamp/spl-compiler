from enum import Enum, auto


class Mnemonic(Enum):

    def __str__(self):
        return self.name.lower()

    MARK_LABEL = auto(),  # Not an actual instruction, but used for marking labels for jumping
    AAA = auto(),
    AAD = auto(),
    AAM = auto(),
    AAS = auto(),
    ADC = auto(),
    ADCX = auto(),
    ADD = auto(),
    ADDPD = auto(),
    ADDPS = auto(),
    ADDSD = auto(),
    ADDSS = auto(),
    ADDSUBPD = auto(),
    ADDSUBPS = auto(),
    ADOX = auto(),
    AESDEC = auto(),
    AESDECLAST = auto(),
    AESENC = auto(),
    AESENCLAST = auto(),
    AESIMC = auto(),
    AESKEYGENASSIST = auto(),
    AND = auto(),
    ANDN = auto(),
    ANDNPD = auto(),
    ANDNPS = auto(),
    ANDPD = auto(),
    ANDPS = auto(),
    ARPL = auto(),
    BEXTR = auto(),
    BLENDPD = auto(),
    BLENDPS = auto(),
    BLENDVPD = auto(),
    BLENDVPS = auto(),
    BLSI = auto(),
    BLSMSK = auto(),
    BLSR = auto(),
    BNDCL = auto(),
    BNDCN = auto(),
    BNDCU = auto(),
    BNDLDX = auto(),
    BNDMK = auto(),
    BNDMOV = auto(),
    BNDSTX = auto(),
    BOUND = auto(),
    BSF = auto(),
    BSR = auto(),
    BSWAP = auto(),
    BT = auto(),
    BTC = auto(),
    BTR = auto(),
    BTS = auto(),
    BZHI = auto(),
    CALL = auto(),
    CBW = auto(),
    CDQ = auto(),
    CDQE = auto(),
    CLAC = auto(),
    CLC = auto(),
    CLD = auto(),
    CLFLUSH = auto(),
    CLFLUSHOPT = auto(),
    CLI = auto(),
    CLTS = auto(),
    CLWB = auto(),
    CMC = auto(),
    CMOVA = auto(),
    CMOVAE = auto(),
    CMOVB = auto(),
    CMOVBE = auto(),
    CMOVC = auto(),
    CMOVE = auto(),
    CMOVG = auto(),
    CMOVGE = auto(),
    CMOVL = auto(),
    CMOVLE = auto(),
    CMOVNA = auto(),
    CMOVNAE = auto(),
    CMOVNB = auto(),
    CMOVNBE = auto(),
    CMOVNC = auto(),
    CMOVNE = auto(),
    CMOVNG = auto(),
    CMOVNGE = auto(),
    CMOVNL = auto(),
    CMOVNLE = auto(),
    CMOVNO = auto(),
    CMOVNP = auto(),
    CMOVNS = auto(),
    CMOVNZ = auto(),
    CMOVO = auto(),
    CMOVP = auto(),
    CMOVPE = auto(),
    CMP = auto(),
    CMPPD = auto(),
    CMPPS = auto(),
    CMPS = auto(),
    CMPSB = auto(),
    CMPSD = auto(),
    CMPSQ = auto(),
    CMPSS = auto(),
    CMPSW = auto(),
    CMPXCHG = auto(),
    CMPXCHG16B = auto(),
    CMPXCHG8B = auto(),
    COMISD = auto(),
    COMISS = auto(),
    CPUID = auto(),
    CQO = auto(),
    CRC32 = auto(),
    CVTDQ2PD = auto(),
    CVTDQ2PS = auto(),
    CVTPD2DQ = auto(),
    CVTPD2PI = auto(),
    CVTPD2PS = auto(),
    CVTPI2PD = auto(),
    CVTPI2PS = auto(),
    CVTPS2DQ = auto(),
    CVTPS2PD = auto(),
    CVTPS2PI = auto(),
    CVTSD2SI = auto(),
    CVTSD2SS = auto(),
    CVTSI2SD = auto(),
    CVTSI2SS = auto(),
    CVTSS2SD = auto(),
    CVTSS2SI = auto(),
    CVTTPD2DQ = auto(),
    CVTTPD2PI = auto(),
    CVTTPS2DQ = auto(),
    CVTTPS2PI = auto(),
    CVTTSD2SI = auto(),
    CVTTSS2SI = auto(),
    CWD = auto(),
    CWDE = auto(),
    DAA = auto(),
    DAS = auto(),
    DEC = auto(),
    DIV = auto(),
    DIVPD = auto(),
    DIVPS = auto(),
    DIVSD = auto(),
    DIVSS = auto(),
    DPPD = auto(),
    DPPS = auto(),
    EMMS = auto(),
    ENTER = auto(),
    EXTRACTPS = auto(),
    F2XM1 = auto(),
    FABS = auto(),
    FADD = auto(),
    FADDP = auto(),
    FBLD = auto(),
    FBSTP = auto(),
    FCHS = auto(),
    FCLEX = auto(),
    FCMOVB = auto(),
    FCMOVBE = auto(),
    FCMOVE = auto(),
    FCMOVNB = auto(),
    FCMOVNBE = auto(),
    FCMOVNE = auto(),
    FCMOVNU = auto(),
    FCMOVU = auto(),
    FCOM = auto(),
    FCOMI = auto(),
    FCOMIP = auto(),
    FCOMP = auto(),
    FCOMPP = auto(),
    FCOS = auto(),
    FDECSTP = auto(),
    FDIV = auto(),
    FDIVP = auto(),
    FDIVR = auto(),
    FDIVRP = auto(),
    FFREE = auto(),
    FIADD = auto(),
    FICOM = auto(),
    FICOMP = auto(),
    FIDIV = auto(),
    FIDIVR = auto(),
    FILD = auto(),
    FIMUL = auto(),
    FINCSTP = auto(),
    FINIT = auto(),
    FIST = auto(),
    FISTP = auto(),
    FISTTP = auto(),
    FISUB = auto(),
    FISUBR = auto(),
    FLD = auto(),
    FLD1 = auto(),
    FLDCW = auto(),
    FLDENV = auto(),
    FLDL2E = auto(),
    FLDL2T = auto(),
    FLDLG2 = auto(),
    FLDLN2 = auto(),
    FLDPI = auto(),
    FLDZ = auto(),
    FMUL = auto(),
    FMULP = auto(),
    FNCLEX = auto(),
    FNINIT = auto(),
    FNOP = auto(),
    FNSAVE = auto(),
    FNSTCW = auto(),
    FNSTENV = auto(),
    FNSTSW = auto(),
    FPATAN = auto(),
    FPREM = auto(),
    FPREM1 = auto(),
    FPTAN = auto(),
    FRNDINT = auto(),
    FRSTOR = auto(),
    FSAVE = auto(),
    FSCALE = auto(),
    FSIN = auto(),
    FSINCOS = auto(),
    FSQRT = auto(),
    FST = auto(),
    FSTCW = auto(),
    FSTENV = auto(),
    FSTP = auto(),
    FSTSW = auto(),
    FSUB = auto(),
    FSUBP = auto(),
    FSUBR = auto(),
    FSUBRP = auto(),
    FTST = auto(),
    FUCOM = auto(),
    FUCOMI = auto(),
    FUCOMIP = auto(),
    FUCOMP = auto(),
    FUCOMPP = auto(),
    FWAIT = auto(),
    FXAM = auto(),
    FXCH = auto(),
    FXRSTOR = auto(),
    FXRSTOR64 = auto(),
    FXSAVE = auto(),
    FXSAVE64 = auto(),
    FXTRACT = auto(),
    FYL2X = auto(),
    FYL2XP1 = auto(),
    HADDPD = auto(),
    HADDPS = auto(),
    HLT = auto(),
    HSUBPD = auto(),
    HSUBPS = auto(),
    IDIV = auto(),
    IMUL = auto(),
    IN = auto(),
    INC = auto(),
    INS = auto(),
    INSB = auto(),
    INSD = auto(),
    INSERTPS = auto(),
    INSW = auto(),
    INT = auto(),
    INTO = auto(),
    INVD = auto(),
    INVLPG = auto(),
    INVPCID = auto(),
    IRET = auto(),
    IRETD = auto(),
    IRETQ = auto(),
    JA = auto(),
    JAE = auto(),
    JB = auto(),
    JBE = auto(),
    JC = auto(),
    JCXZ = auto(),
    JE = auto(),
    JECXZ = auto(),
    JG = auto(),
    JGE = auto(),
    JL = auto(),
    JLE = auto(),
    JMP = auto(),
    JNA = auto(),
    JNAE = auto(),
    JNB = auto(),
    JNBE = auto(),
    JNC = auto(),
    JNE = auto(),
    JNG = auto(),
    JNGE = auto(),
    JNL = auto(),
    JNLE = auto(),
    JNO = auto(),
    JNP = auto(),
    JNS = auto(),
    JNZ = auto(),
    JO = auto(),
    JP = auto(),
    JPE = auto(),
    JPO = auto(),
    JRCXZ = auto(),
    JS = auto(),
    JZ = auto(),
    KADDB = auto(),
    KADDD = auto(),
    KADDQ = auto(),
    KADDW = auto(),
    KANDB = auto(),
    KANDD = auto(),
    KANDNB = auto(),
    KANDND = auto(),
    KANDNQ = auto(),
    KANDNW = auto(),
    KANDQ = auto(),
    KANDW = auto(),
    KMOVB = auto(),
    KMOVD = auto(),
    KMOVQ = auto(),
    KMOVW = auto(),
    KNOTB = auto(),
    KNOTD = auto(),
    KNOTQ = auto(),
    KNOTW = auto(),
    KORB = auto(),
    KORD = auto(),
    KORQ = auto(),
    KORTESTB = auto(),
    KORTESTD = auto(),
    KORTESTQ = auto(),
    KORTESTW = auto(),
    KORW = auto(),
    KSHIFTLB = auto(),
    KSHIFTLD = auto(),
    KSHIFTLQ = auto(),
    KSHIFTLW = auto(),
    KSHIFTRB = auto(),
    KSHIFTRD = auto(),
    KSHIFTRQ = auto(),
    KSHIFTRW = auto(),
    KTESTB = auto(),
    KTESTD = auto(),
    KTESTQ = auto(),
    KTESTW = auto(),
    KUNPCKBW = auto(),
    KUNPCKDQ = auto(),
    KUNPCKWD = auto(),
    KXNORB = auto(),
    KXNORD = auto(),
    KXNORQ = auto(),
    KXNORW = auto(),
    KXORB = auto(),
    KXORD = auto(),
    KXORQ = auto(),
    KXORW = auto(),
    LAHF = auto(),
    LAR = auto(),
    LDDQU = auto(),
    LDMXCSR = auto(),
    LDS = auto(),
    LEA = auto(),
    LEAVE = auto(),
    LES = auto(),
    LFENCE = auto(),
    LFS = auto(),
    LGDT = auto(),
    LGS = auto(),
    LIDT = auto(),
    LLDT = auto(),
    LMSW = auto(),
    LOCK = auto(),
    LODS = auto(),
    LODSB = auto(),
    LODSD = auto(),
    LODSQ = auto(),
    LODSW = auto(),
    LOOP = auto(),
    LOOPE = auto(),
    LOOPNE = auto(),
    LSL = auto(),
    LSS = auto(),
    LTR = auto(),
    LZCNT = auto(),
    MASKMOVDQU = auto(),
    MASKMOVQ = auto(),
    MAXPD = auto(),
    MAXPS = auto(),
    MAXSD = auto(),
    MAXSS = auto(),
    MFENCE = auto(),
    MINPD = auto(),
    MINPS = auto(),
    MINSD = auto(),
    MINSS = auto(),
    MONITOR = auto(),
    MOV = auto(),
    MOVAPD = auto(),
    MOVAPS = auto(),
    MOVBE = auto(),
    MOVD = auto(),
    MOVDDUP = auto(),
    MOVDQ2Q = auto(),
    MOVDQA = auto(),
    MOVDQU = auto(),
    MOVHLPS = auto(),
    MOVHPD = auto(),
    MOVHPS = auto(),
    MOVLHPS = auto(),
    MOVLPD = auto(),
    MOVLPS = auto(),
    MOVMSKPD = auto(),
    MOVMSKPS = auto(),
    MOVNTDQ = auto(),
    MOVNTDQA = auto(),
    MOVNTI = auto(),
    MOVNTPD = auto(),
    MOVNTPS = auto(),
    MOVNTQ = auto(),
    MOVQ = auto(),
    MOVQ2DQ = auto(),
    MOVS = auto(),
    MOVSB = auto(),
    MOVSD = auto(),
    MOVSHDUP = auto(),
    MOVSLDUP = auto(),
    MOVSQ = auto(),
    MOVSS = auto(),
    MOVSW = auto(),
    MOVSX = auto(),
    MOVSXD = auto(),
    MOVUPD = auto(),
    MOVUPS = auto(),
    MOVZX = auto(),
    MPSADBW = auto(),
    MUL = auto(),
    MULPD = auto(),
    MULPS = auto(),
    MULSD = auto(),
    MULSS = auto(),
    MULX = auto(),
    MWAIT = auto(),
    NEG = auto(),
    NOP = auto(),
    NOT = auto(),
    OR = auto(),
    ORPD = auto(),
    ORPS = auto(),
    OUT = auto(),
    OUTS = auto(),
    OUTSB = auto(),
    OUTSD = auto(),
    OUTSW = auto(),
    PABSB = auto(),
    PABSD = auto(),
    PABSW = auto(),
    PACKSSDW = auto(),
    PACKSSWB = auto(),
    PACKUSDW = auto(),
    PACKUSWB = auto(),
    PADDB = auto(),
    PADDD = auto(),
    PADDQ = auto(),
    PADDSB = auto(),
    PADDSW = auto(),
    PADDUSB = auto(),
    PADDUSW = auto(),
    PADDW = auto(),
    PALIGNR = auto(),
    PAND = auto(),
    PANDN = auto(),
    PAUSE = auto(),
    PAVGB = auto(),
    PAVGW = auto(),
    PBLENDVB = auto(),
    PBLENDW = auto(),
    PCLMULQDQ = auto(),
    PCMPEQB = auto(),
    PCMPEQD = auto(),
    PCMPEQQ = auto(),
    PCMPEQW = auto(),
    PCMPESTRI = auto(),
    PCMPESTRM = auto(),
    PCMPGTB = auto(),
    PCMPGTD = auto(),
    PCMPGTQ = auto(),
    PCMPGTW = auto(),
    PCMPISTRI = auto(),
    PCMPISTRM = auto(),
    PDEP = auto(),
    PEXT = auto(),
    PEXTRB = auto(),
    PEXTRD = auto(),
    PEXTRQ = auto(),
    PEXTRW = auto(),
    PHADDD = auto(),
    PHADDSW = auto(),
    PHADDW = auto(),
    PHMINPOSUW = auto(),
    PHSUBD = auto(),
    PHSUBSW = auto(),
    PHSUBW = auto(),
    PINSRB = auto(),
    PINSRD = auto(),
    PINSRQ = auto(),
    PINSRW = auto(),
    PMADDUBSW = auto(),
    PMADDWD = auto(),
    PMAXSB = auto(),
    PMAXSD = auto(),
    PMAXSW = auto(),
    PMAXUB = auto(),
    PMAXUD = auto(),
    PMAXUW = auto(),
    PMINSB = auto(),
    PMINSD = auto(),
    PMINSW = auto(),
    PMINUB = auto(),
    PMINUD = auto(),
    PMINUW = auto(),
    PMOVMSKB = auto(),
    PMOVSXBD = auto(),
    PMOVSXBQ = auto(),
    PMOVSXBW = auto(),
    PMOVSXDQ = auto(),
    PMOVSXWD = auto(),
    PMOVSXWQ = auto(),
    PMOVZXBD = auto(),
    PMOVZXBQ = auto(),
    PMOVZXBW = auto(),
    PMOVZXDQ = auto(),
    PMOVZXWD = auto(),
    PMOVZXWQ = auto(),
    PMULDQ = auto(),
    PMULHRSW = auto(),
    PMULHUW = auto(),
    PMULHW = auto(),
    PMULLD = auto(),
    PMULLW = auto(),
    PMULUDQ = auto(),
    POP = auto(),
    POPA = auto(),
    POPAD = auto(),
    POPCNT = auto(),
    POPF = auto(),
    POPFD = auto(),
    POPFQ = auto(),
    POR = auto(),
    PREFETCHNTA = auto(),
    PREFETCHT0 = auto(),
    PREFETCHT1 = auto(),
    PREFETCHT2 = auto(),
    PREFETCHW = auto(),
    PREFETCHWT1 = auto(),
    PSADBW = auto(),
    PSHUFB = auto(),
    PSHUFD = auto(),
    PSHUFHW = auto(),
    PSHUFLW = auto(),
    PSHUFW = auto(),
    PSIGNB = auto(),
    PSIGND = auto(),
    PSIGNW = auto(),
    PSLLD = auto(),
    PSLLDQ = auto(),
    PSLLQ = auto(),
    PSLLW = auto(),
    PSRAD = auto(),
    PSRAW = auto(),
    PSRLD = auto(),
    PSRLDQ = auto(),
    PSRLQ = auto(),
    PSRLW = auto(),
    PSUBB = auto(),
    PSUBD = auto(),
    PSUBQ = auto(),
    PSUBSB = auto(),
    PSUBSW = auto(),
    PSUBUSB = auto(),
    PSUBUSW = auto(),
    PSUBW = auto(),
    PTEST = auto(),
    PTWRITE = auto(),
    PUNPCKHBW = auto(),
    PUNPCKHDQ = auto(),
    PUNPCKHQDQ = auto(),
    PUNPCKHWD = auto(),
    PUNPCKLBW = auto(),
    PUNPCKLDQ = auto(),
    PUNPCKLQDQ = auto(),
    PUNPCKLWD = auto(),
    PUSH = auto(),
    PUSHA = auto(),
    PUSHAD = auto(),
    PUSHF = auto(),
    PUSHFD = auto(),
    PUSHFQ = auto(),
    PXOR = auto(),
    RCL = auto(),
    RCPPS = auto(),
    RCPSS = auto(),
    RCR = auto(),
    RDFSBASE = auto(),
    RDGSBASE = auto(),
    RDMSR = auto(),
    RDPID = auto(),
    RDPKRU = auto(),
    RDPMC = auto(),
    RDRAND = auto(),
    RDSEED = auto(),
    RDTSC = auto(),
    RDTSCP = auto(),
    RET = auto(),
    ROL = auto(),
    ROR = auto(),
    RORX = auto(),
    ROUNDPD = auto(),
    ROUNDPS = auto(),
    ROUNDSD = auto(),
    ROUNDSS = auto(),
    RSM = auto(),
    RSQRTPS = auto(),
    RSQRTSS = auto(),
    SAHF = auto(),
    SAL = auto(),
    SAR = auto(),
    SARX = auto(),
    SBB = auto(),
    SCAS = auto(),
    SCASB = auto(),
    SCASD = auto(),
    SCASQ = auto(),
    SCASW = auto(),
    SETA = auto(),
    SETAE = auto(),
    SETB = auto(),
    SETBE = auto(),
    SETC = auto(),
    SETE = auto(),
    SETG = auto(),
    SETGE = auto(),
    SETL = auto(),
    SETLE = auto(),
    SETNA = auto(),
    SETNAE = auto(),
    SETNB = auto(),
    SETNBE = auto(),
    SETNC = auto(),
    SETNE = auto(),
    SETNG = auto(),
    SETNGE = auto(),
    SETNL = auto(),
    SETNLE = auto(),
    SFENCE = auto(),
    SGDT = auto(),
    SHA1MSG1 = auto(),
    SHA1MSG2 = auto(),
    SHA1NEXTE = auto(),
    SHA1RNDS4 = auto(),
    SHA256MSG1 = auto(),
    SHA256MSG2 = auto(),
    SHA256RNDS2 = auto(),
    SHL = auto(),
    SHLD = auto(),
    SHLX = auto(),
    SHR = auto(),
    SHRD = auto(),
    SHRX = auto(),
    SHUFPD = auto(),
    SHUFPS = auto(),
    SIDT = auto(),
    SLDT = auto(),
    SMSW = auto(),
    SQRTPD = auto(),
    SQRTPS = auto(),
    SQRTSD = auto(),
    SQRTSS = auto(),
    STAC = auto(),
    STC = auto(),
    STD = auto(),
    STI = auto(),
    STMXCSR = auto(),
    STOS = auto(),
    STOSB = auto(),
    STOSD = auto(),
    STOSQ = auto(),
    STOSW = auto(),
    STR = auto(),
    SUB = auto(),
    SUBPD = auto(),
    SUBPS = auto(),
    SUBSD = auto(),
    SUBSS = auto(),
    SWAPGS = auto(),
    SYSCALL = auto(),
    SYSENTER = auto(),
    SYSEXIT = auto(),
    SYSRET = auto(),
    TEST = auto(),
    TZCNT = auto(),
    UCOMISD = auto(),
    UCOMISS = auto(),
    UD0 = auto(),
    UD1 = auto(),
    UD2 = auto(),
    UNPCKHPD = auto(),
    UNPCKHPS = auto(),
    UNPCKLPD = auto(),
    UNPCKLPS = auto(),
    VADDPD = auto(),
    VADDPS = auto(),
    VADDSD = auto(),
    VADDSS = auto(),
    VADDSUBPD = auto(),
    VADDSUBPS = auto(),
    VAESDEC = auto(),
    VAESDECLAST = auto(),
    VAESENC = auto(),
    VAESENCLAST = auto(),
    VAESIMC = auto(),
    VAESKEYGENASSIST = auto(),
    VALIGND = auto(),
    VALIGNQ = auto(),
    VANDNPD = auto(),
    VANDNPS = auto(),
    VANDPD = auto(),
    VANDPS = auto(),
    VBLENDMPD = auto(),
    VBLENDMPS = auto(),
    VBLENDPD = auto(),
    VBLENDPS = auto(),
    VBLENDVPD = auto(),
    VBLENDVPS = auto(),
    VBROADCASTF128 = auto(),
    VBROADCASTF32X2 = auto(),
    VBROADCASTF32X4 = auto(),
    VBROADCASTF64X2 = auto(),
    VBROADCASTI128 = auto(),
    VBROADCASTI32x2 = auto(),
    VBROADCASTI32X4 = auto(),
    VBROADCASTI32X8 = auto(),
    VBROADCASTI64X2 = auto(),
    VBROADCASTI64X4 = auto(),
    VBROADCASTSD = auto(),
    VBROADCASTSS = auto(),
    VCMPPD = auto(),
    VCMPPS = auto(),
    VCMPSD = auto(),
    VCMPSS = auto(),
    VCOMISD = auto(),
    VCOMISS = auto(),
    VCOMPRESSPD = auto(),
    VCOMPRESSPS = auto(),
    VCVTDQ2PD = auto(),
    VCVTDQ2PS = auto(),
    VCVTPD2DQ = auto(),
    VCVTPD2PS = auto(),
    VCVTPD2QQ = auto(),
    VCVTPD2UDQ = auto(),
    VCVTPD2UQQ = auto(),
    VCVTPH2PS = auto(),
    VCVTPS2DQ = auto(),
    VCVTPS2PD = auto(),
    VCVTPS2PH = auto(),
    VCVTPS2QQ = auto(),
    VCVTPS2UDQ = auto(),
    VCVTPS2UQQ = auto(),
    VCVTQQ2PD = auto(),
    VCVTQQ2PS = auto(),
    VCVTSD2SI = auto(),
    VCVTSD2SS = auto(),
    VCVTSD2USI = auto(),
    VCVTSI2SD = auto(),
    VCVTSI2SS = auto(),
    VCVTSS2SD = auto(),
    VCVTSS2SI = auto(),
    VCVTSS2USI = auto(),
    VCVTTPD2DQ = auto(),
    VCVTTPD2QQ = auto(),
    VCVTTPD2UDQ = auto(),
    VCVTTPD2UQQ = auto(),
    VCVTTPS2DQ = auto(),
    VCVTTPS2QQ = auto(),
    VCVTTPS2UDQ = auto(),
    VCVTTPS2UQQ = auto(),
    VCVTTSD2SI = auto(),
    VCVTTSD2USI = auto(),
    VCVTTSS2SI = auto(),
    VCVTTSS2USI = auto(),
    VCVTUDQ2PD = auto(),
    VCVTUDQ2PS = auto(),
    VCVTUQQ2PD = auto(),
    VCVTUQQ2PS = auto(),
    VCVTUSI2SD = auto(),
    VCVTUSI2SS = auto(),
    VDBPSADBW = auto(),
    VDIVPD = auto(),
    VDIVPS = auto(),
    VDIVSD = auto(),
    VDIVSS = auto(),
    VDPPD = auto(),
    VDPPS = auto(),
    VERR = auto(),
    VERW = auto(),
    VEXP2PD = auto(),
    VEXP2PS = auto(),
    VEXPANDPD = auto(),
    VEXPANDPS = auto(),
    VEXTRACTF128 = auto(),
    VEXTRACTF32x4 = auto(),
    VEXTRACTF64x4 = auto(),
    VEXTRACTI128 = auto(),
    VEXTRACTI32x4 = auto(),
    VEXTRACTI64x4 = auto(),
    VEXTRACTPS = auto(),
    VFIXUPIMMPD = auto(),
    VFIXUPIMMPS = auto(),
    VFIXUPIMMSD = auto(),
    VFIXUPIMMSS = auto(),
    VFMADD132PD = auto(),
    VFMADD132PS = auto(),
    VFMADD132SD = auto(),
    VFMADD132SS = auto(),
    VFMADD213PD = auto(),
    VFMADD213PS = auto(),
    VFMADD213SD = auto(),
    VFMADD213SS = auto(),
    VFMADD231PD = auto(),
    VFMADD231PS = auto(),
    VFMADD231SD = auto(),
    VFMADD231SS = auto(),
    VFMADDSUB132PD = auto(),
    VFMADDSUB132PS = auto(),
    VFMADDSUB213PD = auto(),
    VFMADDSUB213PS = auto(),
    VFMADDSUB231PD = auto(),
    VFMADDSUB231PS = auto(),
    VFMSUB132PD = auto(),
    VFMSUB132PS = auto(),
    VFMSUB132SD = auto(),
    VFMSUB132SS = auto(),
    VFMSUB213PD = auto(),
    VFMSUB213PS = auto(),
    VFMSUB213SD = auto(),
    VFMSUB213SS = auto(),
    VFMSUB231PD = auto(),
    VFMSUB231PS = auto(),
    VFMSUB231SD = auto(),
    VFMSUB231SS = auto(),
    VFMSUBADD132PD = auto(),
    VFMSUBADD132PS = auto(),
    VFMSUBADD213PD = auto(),
    VFMSUBADD213PS = auto(),
    VFMSUBADD231PD = auto(),
    VFMSUBADD231PS = auto(),
    VFNMADD132PD = auto(),
    VFNMADD132PS = auto(),
    VFNMADD132SD = auto(),
    VFNMADD132SS = auto(),
    VFNMADD213PD = auto(),
    VFNMADD213PS = auto(),
    VFNMADD213SD = auto(),
    VFNMADD213SS = auto(),
    VFNMADD231PD = auto(),
    VFNMADD231PS = auto(),
    VFNMADD231SD = auto(),
    VFNMADD231SS = auto(),
    VFNMSUB132PD = auto(),
    VFNMSUB132PS = auto(),
    VFNMSUB132SD = auto(),
    VFNMSUB132SS = auto(),
    VFNMSUB213PD = auto(),
    VFNMSUB213PS = auto(),
    VFNMSUB213SD = auto(),
    VFNMSUB213SS = auto(),
    VFNMSUB231PD = auto(),
    VFNMSUB231PS = auto(),
    VFNMSUB231SD = auto(),
    VFNMSUB231SS = auto(),
    VFPCLASSPD = auto(),
    VFPCLASSPS = auto(),
    VFPCLASSSD = auto(),
    VFPCLASSSS = auto(),
    VGATHERDPD = auto(),
    VGATHERDPS = auto(),
    VGATHERPF0DPD = auto(),
    VGATHERPF0DPS = auto(),
    VGATHERPF0QPD = auto(),
    VGATHERPF0QPS = auto(),
    VGATHERPF1DPD = auto(),
    VGATHERPF1DPS = auto(),
    VGATHERPF1QPD = auto(),
    VGATHERPF1QPS = auto(),
    VGATHERQPD = auto(),
    VGATHERQPS = auto(),
    VGETEXPPD = auto(),
    VGETEXPPS = auto(),
    VGETEXPSD = auto(),
    VGETEXPSS = auto(),
    VGETMANTPD = auto(),
    VGETMANTPS = auto(),
    VGETMANTSD = auto(),
    VGETMANTSS = auto(),
    VHADDPD = auto(),
    VHADDPS = auto(),
    VHSUBPD = auto(),
    VHSUBPS = auto(),
    VINSERTF128 = auto(),
    VINSERTI128 = auto(),
    VINSERTPS = auto(),
    VLDDQU = auto(),
    VLDMXCSR = auto(),
    VMASKMOVDQU = auto(),
    VMASKMOVPD = auto(),
    VMASKMOVPS = auto(),
    VMAXPD = auto(),
    VMAXPS = auto(),
    VMAXSD = auto(),
    VMAXSS = auto(),
    VMINPD = auto(),
    VMINPS = auto(),
    VMINSD = auto(),
    VMINSS = auto(),
    VMOVAPD = auto(),
    VMOVAPS = auto(),
    VMOVD = auto(),
    VMOVDDUP = auto(),
    VMOVDQA = auto(),
    VMOVDQA32 = auto(),
    VMOVDQA64 = auto(),
    VMOVDQU = auto(),
    VMOVDQU16 = auto(),
    VMOVDQU32 = auto(),
    VMOVDQU64 = auto(),
    VMOVDQU8 = auto(),
    VMOVHLPS = auto(),
    VMOVHPD = auto(),
    VMOVHPS = auto(),
    VMOVLHPS = auto(),
    VMOVLPD = auto(),
    VMOVLPS = auto(),
    VMOVMSKPD = auto(),
    VMOVMSKPS = auto(),
    VMOVNTDQ = auto(),
    VMOVNTDQA = auto(),
    VMOVNTPD = auto(),
    VMOVNTPS = auto(),
    VMOVQ = auto(),
    VMOVSD = auto(),
    VMOVSHDUP = auto(),
    VMOVSLDUP = auto(),
    VMOVSS = auto(),
    VMOVUPD = auto(),
    VMOVUPS = auto(),
    VMPSADBW = auto(),
    VMULPD = auto(),
    VMULPS = auto(),
    VMULSD = auto(),
    VMULSS = auto(),
    VORPD = auto(),
    VORPS = auto(),
    VPABSB = auto(),
    VPABSD = auto(),
    VPABSW = auto(),
    VPACKSSDW = auto(),
    VPACKSSWB = auto(),
    VPACKUSDW = auto(),
    VPACKUSWB = auto(),
    VPADDB = auto(),
    VPADDD = auto(),
    VPADDQ = auto(),
    VPADDSB = auto(),
    VPADDSW = auto(),
    VPADDUSB = auto(),
    VPADDUSW = auto(),
    VPADDW = auto(),
    VPALIGNR = auto(),
    VPAND = auto(),
    VPANDD = auto(),
    VPANDN = auto(),
    VPANDND = auto(),
    VPANDNQ = auto(),
    VPANDQ = auto(),
    VPAVGB = auto(),
    VPAVGW = auto(),
    VPBLENDD = auto(),
    VPBLENDMB = auto(),
    VPBLENDMD = auto(),
    VPBLENDMQ = auto(),
    VPBLENDMW = auto(),
    VPBLENDVB = auto(),
    VPBLENDW = auto(),
    VPBROADCASTB = auto(),
    VPBROADCASTD = auto(),
    VPBROADCASTMB2Q = auto(),
    VPBROADCASTMW2D = auto(),
    VPBROADCASTQ = auto(),
    VPBROADCASTW = auto(),
    VPCLMULQDQ = auto(),
    VPCMPB = auto(),
    VPCMPD = auto(),
    VPCMPEQB = auto(),
    VPCMPEQD = auto(),
    VPCMPEQQ = auto(),
    VPCMPEQW = auto(),
    VPCMPESTRI = auto(),
    VPCMPESTRM = auto(),
    VPCMPGTB = auto(),
    VPCMPGTD = auto(),
    VPCMPGTQ = auto(),
    VPCMPGTW = auto(),
    VPCMPISTRI = auto(),
    VPCMPISTRM = auto(),
    VPCMPQ = auto(),
    VPCMPUB = auto(),
    VPCMPUD = auto(),
    VPCMPUQ = auto(),
    VPCMPUW = auto(),
    VPCMPW = auto(),
    VPCOMPRESSD = auto(),
    VPCOMPRESSQ = auto(),
    VPCONFLICTD = auto(),
    VPCONFLICTQ = auto(),
    VPERM2F128 = auto(),
    VPERM2I128 = auto(),
    VPERMD = auto(),
    VPERMI2D = auto(),
    VPERMI2PD = auto(),
    VPERMI2PS = auto(),
    VPERMI2Q = auto(),
    VPERMI2W = auto(),
    VPERMILPD = auto(),
    VPERMILPS = auto(),
    VPERMPD = auto(),
    VPERMPS = auto(),
    VPERMQ = auto(),
    VPERMT2D = auto(),
    VPERMT2PD = auto(),
    VPERMT2PS = auto(),
    VPERMT2Q = auto(),
    VPERMT2W = auto(),
    VPERMW = auto(),
    VPEXPANDD = auto(),
    VPEXPANDQ = auto(),
    VPEXTRB = auto(),
    VPEXTRD = auto(),
    VPEXTRQ = auto(),
    VPEXTRW = auto(),
    VPGATHERDD = auto(),
    VPGATHERDQ = auto(),
    VPGATHERQD = auto(),
    VPGATHERQQ = auto(),
    VPHADDD = auto(),
    VPHADDSW = auto(),
    VPHADDW = auto(),
    VPHMINPOSUW = auto(),
    VPHSUBD = auto(),
    VPHSUBSW = auto(),
    VPHSUBW = auto(),
    VPINSRB = auto(),
    VPINSRD = auto(),
    VPINSRQ = auto(),
    VPINSRW = auto(),
    VPLZCNTD = auto(),
    VPLZCNTQ = auto(),
    VPMADDUBSW = auto(),
    VPMADDWD = auto(),
    VPMASKMOVD = auto(),
    VPMASKMOVQ = auto(),
    VPMAXSB = auto(),
    VPMAXSD = auto(),
    VPMAXSW = auto(),
    VPMAXUB = auto(),
    VPMAXUD = auto(),
    VPMAXUQ = auto(),
    VPMAXUW = auto(),
    VPMINSB = auto(),
    VPMINSD = auto(),
    VPMINSQ = auto(),
    VPMINSW = auto(),
    VPMINUB = auto(),
    VPMINUD = auto(),
    VPMINUQ = auto(),
    VPMINUW = auto(),
    VPMOVB2M = auto(),
    VPMOVD2M = auto(),
    VPMOVDB = auto(),
    VPMOVDW = auto(),
    VPMOVM2B = auto(),
    VPMOVM2D = auto(),
    VPMOVM2Q = auto(),
    VPMOVM2W = auto(),
    VPMOVMSKB = auto(),
    VPMOVQ2M = auto(),
    VPMOVQB = auto(),
    VPMOVQD = auto(),
    VPMOVQW = auto(),
    VPMOVSDB = auto(),
    VPMOVSDW = auto(),
    VPMOVSQB = auto(),
    VPMOVSQD = auto(),
    VPMOVSQW = auto(),
    VPMOVSWB = auto(),
    VPMOVSXBD = auto(),
    VPMOVSXBQ = auto(),
    VPMOVSXBW = auto(),
    VPMOVSXDQ = auto(),
    VPMOVSXWD = auto(),
    VPMOVSXWQ = auto(),
    VPMOVUSDB = auto(),
    VPMOVUSDW = auto(),
    VPMOVUSQB = auto(),
    VPMOVUSQD = auto(),
    VPMOVUSQW = auto(),
    VPMOVUSWB = auto(),
    VPMOVW2M = auto(),
    VPMOVWB = auto(),
    VPMOVZXBD = auto(),
    VPMOVZXBQ = auto(),
    VPMOVZXBW = auto(),
    VPMOVZXDQ = auto(),
    VPMOVZXWD = auto(),
    VPMOVZXWQ = auto(),
    VPMULDQ = auto(),
    VPMULHRSW = auto(),
    VPMULHUW = auto(),
    VPMULHW = auto(),
    VPMULLD = auto(),
    VPMULLQ = auto(),
    VPMULLW = auto(),
    VPMULUDQ = auto(),
    VPOR = auto(),
    VPORD = auto(),
    VPORQ = auto(),
    VPROLD = auto(),
    VPROLQ = auto(),
    VPROLVD = auto(),
    VPROLVQ = auto(),
    VPRORD = auto(),
    VPRORQ = auto(),
    VPRORVD = auto(),
    VPRORVQ = auto(),
    VPSADBW = auto(),
    VPSCATTERDD = auto(),
    VPSCATTERDQ = auto(),
    VPSCATTERQD = auto(),
    VPSCATTERQQ = auto(),
    VPSHUFB = auto(),
    VPSHUFD = auto(),
    VPSHUFHW = auto(),
    VPSHUFLW = auto(),
    VPSIGNB = auto(),
    VPSIGND = auto(),
    VPSIGNW = auto(),
    VPSLLD = auto(),
    VPSLLDQ = auto(),
    VPSLLQ = auto(),
    VPSLLVD = auto(),
    VPSLLVQ = auto(),
    VPSLLVW = auto(),
    VPSLLW = auto(),
    VPSRAD = auto(),
    VPSRAQ = auto(),
    VPSRAVD = auto(),
    VPSRAVQ = auto(),
    VPSRAVW = auto(),
    VPSRAW = auto(),
    VPSRLD = auto(),
    VPSRLDQ = auto(),
    VPSRLQ = auto(),
    VPSRLVD = auto(),
    VPSRLVQ = auto(),
    VPSRLVW = auto(),
    VPSRLW = auto(),
    VPSUBB = auto(),
    VPSUBD = auto(),
    VPSUBQ = auto(),
    VPSUBSB = auto(),
    VPSUBSW = auto(),
    VPSUBUSB = auto(),
    VPSUBUSW = auto(),
    VPSUBW = auto(),
    VPTERNLOGD = auto(),
    VPTERNLOGQ = auto(),
    VPTEST = auto(),
    VPTESTMB = auto(),
    VPTESTMD = auto(),
    VPTESTMQ = auto(),
    VPTESTMW = auto(),
    VPTESTNMB = auto(),
    VPTESTNMD = auto(),
    VPTESTNMQ = auto(),
    VPTESTNMW = auto(),
    VPUNPCKHBW = auto(),
    VPUNPCKHDQ = auto(),
    VPUNPCKHQDQ = auto(),
    VPUNPCKHWD = auto(),
    VPUNPCKLBW = auto(),
    VPUNPCKLDQ = auto(),
    VPUNPCKLQDQ = auto(),
    VPUNPCKLWD = auto(),
    VPXOR = auto(),
    VPXORD = auto(),
    VPXORQ = auto(),
    VRANGEPD = auto(),
    VRANGEPS = auto(),
    VRANGESD = auto(),
    VRANGESS = auto(),
    VRCP14PD = auto(),
    VRCP14PS = auto(),
    VRCP14SD = auto(),
    VRCP14SS = auto(),
    VRCP28PD = auto(),
    VRCP28PS = auto(),
    VRCP28SD = auto(),
    VRCP28SS = auto(),
    VRCPPS = auto(),
    VRCPSS = auto(),
    VREDUCEPD = auto(),
    VREDUCEPS = auto(),
    VREDUCESD = auto(),
    VREDUCESS = auto(),
    VRNDSCALEPD = auto(),
    VRNDSCALEPS = auto(),
    VRNDSCALESD = auto(),
    VRNDSCALESS = auto(),
    VROUNDPD = auto(),
    VROUNDPS = auto(),
    VROUNDSD = auto(),
    VROUNDSS = auto(),
    VRSQRT14PD = auto(),
    VRSQRT14PS = auto(),
    VRSQRT14SD = auto(),
    VRSQRT14SS = auto(),
    VRSQRT28PD = auto(),
    VRSQRT28PS = auto(),
    VRSQRT28SD = auto(),
    VRSQRT28SS = auto(),
    VRSQRTPS = auto(),
    VRSQRTSS = auto(),
    VSCALEFPD = auto(),
    VSCALEFPS = auto(),
    VSCALEFSD = auto(),
    VSCALEFSS = auto(),
    VSCATTERDPD = auto(),
    VSCATTERDPS = auto(),
    VSCATTERPF0DPD = auto(),
    VSCATTERPF0DPS = auto(),
    VSCATTERPF0QPD = auto(),
    VSCATTERPF0QPS = auto(),
    VSCATTERPF1DPD = auto(),
    VSCATTERPF1DPS = auto(),
    VSCATTERPF1QPD = auto(),
    VSCATTERPF1QPS = auto(),
    VSCATTERQPD = auto(),
    VSCATTERQPS = auto(),
    VSHUFF32x4 = auto(),
    VSHUFF64x2 = auto(),
    VSHUFI32x4 = auto(),
    VSHUFI64x2 = auto(),
    VSHUFPD = auto(),
    VSHUFPS = auto(),
    VSQRTPD = auto(),
    VSQRTPS = auto(),
    VSQRTSD = auto(),
    VSQRTSS = auto(),
    VSTMXCSR = auto(),
    VSUBPD = auto(),
    VSUBPS = auto(),
    VSUBSD = auto(),
    VSUBSS = auto(),
    VTESTPD = auto(),
    VTESTPS = auto(),
    VUCOMISD = auto(),
    VUCOMISS = auto(),
    VUNPCKHPD = auto(),
    VUNPCKHPS = auto(),
    VUNPCKLPD = auto(),
    VUNPCKLPS = auto(),
    VXORPD = auto(),
    VXORPS = auto(),
    VZEROALL = auto(),
    VZEROUPPER = auto(),
    WAIT = auto(),
    WBINVD = auto(),
    WRFSBASE = auto(),
    WRGSBASE = auto(),
    WRMSR = auto(),
    WRPKRU = auto(),
    XABORT = auto(),
    XACQUIRE = auto(),
    XADD = auto(),
    XBEGIN = auto(),
    XCHG = auto(),
    XEND = auto(),
    XGETBV = auto(),
    XLAT = auto(),
    XLATB = auto(),
    XOR = auto(),
    XORPD = auto(),
    XORPS = auto(),
    XRELEASE = auto(),
    XRSTOR = auto(),
    XRSTOR64 = auto(),
    XRSTORS = auto(),
    XRSTORS64 = auto(),
    XSAVE = auto(),
    XSAVE64 = auto(),
    XSAVEC = auto(),
    XSAVEC64 = auto(),
    XSAVEOPT = auto(),
    XSAVEOPT64 = auto(),
    XSAVES = auto(),
    XSAVES64 = auto(),
    XSETBV = auto(),
    XTEST = auto(),