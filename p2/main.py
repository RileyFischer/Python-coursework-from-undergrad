{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This line is a comment because it starts with a pound sign (#). That                                                                                                                                         \n",
    "# means Python ignores it.  A comment is just for a human reading the                                                                                                                                          \n",
    "# code.  This project involves 20 small problems to give you practice                                                                                                                                          \n",
    "# with operators, types, and boolean logic.  We'll give you directions                                                                                                                                         \n",
    "# (as comments) on what to do for each problem.                                                                                                                                                                \n",
    "#                                                                                                                                                                                                              \n",
    "# Before you get started, please tell us who you are, putting your\n",
    "# Net ID and your partner's Net ID below (or none if your working solo)                                                                                                                                      \n",
    "\n",
    "# project: p2\n",
    "# submitter: rjfischer\n",
    "# partner: none"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "2"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q1: what is 1+1?\n",
    "\n",
    "# we did this one for you :)\n",
    "\n",
    "1+1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "4"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q2: what is 2+2?\n",
    "\n",
    "2+2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "int"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q3: what is the type of 220?\n",
    "\n",
    "# we did this one for you too...\n",
    "\n",
    "type(220)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "float"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q4: what is the type of 220/4?\n",
    "\n",
    "type(220/4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "int"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q5: what is the type of 220//4?\n",
    "\n",
    "type(220//4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "str"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q6: what is the type of \"220\"?  Note the quotes!\n",
    "\n",
    "type(\"200\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "str"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q7: what is the type of \"False\"?  Note the quotes!\n",
    "\n",
    "type(\"False\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "bool"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q8: what is the type of True?\n",
    "\n",
    "type(True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "bool"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q9: what is the type of 1000<999?\n",
    "\n",
    "type(1000<999)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "220"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q10: what is two hundred plus twenty?\n",
    "\n",
    "# fix the below to make Python do an addition that produces 220\n",
    "\n",
    "200 + 20"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "':):):):):)'"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q11: please fix the following to display 5 smileys\n",
    "\n",
    "\":)\" * 5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "42"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q12: please fix the following to get 42\n",
    "\n",
    "6* 7"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "216"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q13: what is the volume of a cube with side length of 6?\n",
    "\n",
    "# oops, it is currently computing the area of a square (please fix)\n",
    "\n",
    "6 ** 3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1620"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q14: you start with 20 dollars and triple your money every decade.\n",
    "# how much will you have after 4 decades?\n",
    "\n",
    "(20*(3**4))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q15: fix the Python logic to match the English\n",
    "\n",
    "# In English: 220 is less than 320 and greater than 400\n",
    "\n",
    "# In Python:\n",
    "440<220 < 320"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q16: change ONLY the value of x to get True for the output\n",
    "\n",
    "x = -35\n",
    "\n",
    "x < -30 and x > -40"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q17: change ONLY the value of x to get True for the output\n",
    "\n",
    "x = 250\n",
    "\n",
    "(x > 200 and x < 251) and (x > 249 and x < 300)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q18: what???\n",
    "\n",
    "x = 4\n",
    "\n",
    "# fix the following logic so we get True, not 4.\n",
    "# The correct logic should check whether x is either\n",
    "# -4 or 4.  The problem is with types: to the left\n",
    "# of the or, we have a boolean, and to the right of\n",
    "# the or, we have an integer.  This semester, we will\n",
    "# always try to have a boolean to both the left and\n",
    "# right of logical operators such as or.\n",
    "\n",
    "x == -4 or x==4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q19: we should win!\n",
    "\n",
    "number = 36\n",
    "\n",
    "# There are three winners, with numbers 36, 323, and 325.\n",
    "# The following should output True if number is changed\n",
    "# to be any of these (but the logic is currently wrong).\n",
    "#\n",
    "# Please update the following expression so we get True\n",
    "# if the number variable is changed to any of the winning\n",
    "# options.\n",
    "\n",
    "# Did we win?\n",
    "number == 36 or number == 323 or number == 325"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "100.48"
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#q20: what is the volume of a cylinder with radius 4 and height 2?\n",
    "#you may assume PI is 3.14 if you like (a close answer is good enough)\n",
    "\n",
    "(3.14*(4**2))*2\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
