\LoadClassWithOptions{beamer}[lualatex, hyperref={pdfencoding=unicode}]

\RequirePackage{polyglossia}
\setdefaultlanguage{french}

\usefonttheme{professionalfonts}
\RequirePackage{fontspec}
\setmonofont{Inconsolata}

\RequirePackage{shellesc}

\RequirePackage{float}
%\RequirePackage{hyperref}
\RequirePackage{unicode-math}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{minted}
\RequirePackage{upquote}

\hypersetup{pdfencoding=auto}

% Couleurs

\definecolor{vert}{RGB}{78,100,26}
\definecolor{violet}{RGB}{130,25,111}
\definecolor{orange}{RGB}{234,91,12}
\definecolor{rouge}{RGB}{230,56,18}
\definecolor{beige}{RGB}{242,238,231}
\definecolor{bleu}{RGB}{0,74,155}

\hypersetup{
    colorlinks=true,       % false: boxed links; true: colored links
    linkcolor=rouge,
    urlcolor=bleu      % color of external links
}

% Options beamer

\setbeamercolor{structure}{fg=rouge, bg=beige}
\setbeamercolor{block body}{bg=beige}
\setbeamertemplate{navigation symbols}{}
\beamertemplatefootpagenumber


% En-tête

\newcommand{\course}[1]{\def \thecoursename {#1}}
\newcommand{\curriculum}[1]{\def \thecurriculum {#1}}
\newcommand{\myyear}[1]{\def \theyear {#1}}
\newcommand{\mytitle}[1]{\def \thesubtitle {#1}}

\titlegraphic{\includegraphics[scale=.3]{../../../latex/UPEM-IGM-V1_300dpi.png}}
\title{\thecoursename}
\institute{\thecurriculum}
\date{{\small \theyear}}
\subtitle{\thesubtitle}
\author{}


% Environnements / théorèmes

\theoremstyle{definition}
\newtheorem{exemple}{Exemple}
\newtheorem{probleme}{Problème}
\theoremstyle{plain} % switch back to the default theorem style


% Commandes diverses

\newcommand{\defterm}[1]{{\color{orange} #1}}
\newcommand{\warning}[1]{{\textcolor{rouge}{#1}}}

\newenvironment{warningbox} {
\begin{beamerboxesrounded}{}
\begin{minipage}{.1\textwidth}
\includegraphics[scale=.03]{../../../latex/warning.png}
\end{minipage}
\begin{minipage}{.8\textwidth}
}{
\end{minipage}
\end{beamerboxesrounded}
}

% Options TiKZ

\usetikzlibrary{quotes}
\usetikzlibrary{arrows,positioning}

\tikzstyle{val}=[rectangle,draw]
\tikzstyle{var}=[rectangle,rounded corners=1.5ex,draw,bleu,minimum size=3ex]
\tikzstyle{aff}=[->,thick]
\tikzset{
  every node/.style={font=\footnotesize},
  instr/.style={rectangle,draw=black!70},
  test/.style={rectangle,rounded corners,draw=bleu!70,text=bleu},
  every edge/.style={>=stealth,semithick,bend angle=45,draw,->},
  every edge quotes/.style={inner sep=.5em,font=\scriptsize,color=orange},
  vrai/.style={left,"vrai"},
  faux/.style={right,"faux"},
}

\newcommand{\tableau}[2]{
    \draw[step=.5cm,line width=2pt,line cap=rect] (0,0) grid (#1*0.5,#2*0.5);
}

% Options minted

\setminted{
linenos=False,
mathescape,
texcomments,
escapeinside=||,
fontfamily=tt
}
\newminted[python]{python3}{}
\newminted[pycon]{pycon}{python3}
\newminted[shell]{shell-session}{}
\newmintinline[pyinline]{python3}{}
\newmintedfile[pyfile]{python3}{}

\newcommand{\code}[2][]{\pyinline[#1]!#2!}

\newenvironment{pyframe}[2][\linewidth]{%
  \VerbatimEnvironment
  \begin{center}%
  \begin{minipage}{#1}%
  \begin{beamerboxesrounded}{#2}%
  \begin{python}}
{%
  \end{python}%
  \end{beamerboxesrounded}%
  \end{minipage}%
  \end{center}}
