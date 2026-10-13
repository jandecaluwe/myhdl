import pytest

from myhdl import (block, always_comb, instance, Signal, intbv, delay,
                   StopSimulation)


@block
def divmodBench(amin, bmin):
    a = Signal(intbv(0, min=amin, max=16))
    b = Signal(intbv(1, min=bmin, max=16))
    quotient = Signal(intbv(0, min=-32, max=32))
    remainder = Signal(intbv(0, min=-16, max=16))

    @always_comb
    def outputs():
        if b != 0:
            quotient.next = a // b
            remainder.next = a % b

    @instance
    def stimulus():
        for aa in range(amin, 16):
            for bb in range(bmin, 16):
                if bb != 0:
                    a.next = aa
                    b.next = bb
                    yield delay(10)
                    q = int(a)
                    r = int(a)
                    q //= b
                    r %= b
                    print(int(quotient), int(remainder), q, r)
                    qpos = a // 3
                    rpos = a % 3
                    qneg = a // -3
                    rneg = a % -3
                    print(qpos, rpos, qneg, rneg)
                    qpos = 3 // b
                    rpos = 3 % b
                    qneg = -3 // b
                    rneg = -3 % b
                    print(qpos, rpos, qneg, rneg)
        raise StopSimulation

    return outputs, stimulus


@pytest.mark.parametrize('amin, bmin', [(-8, -8), (-8, 0), (0, -8), (0, 0)])
def test_divmod(amin, bmin):
    assert divmodBench(amin, bmin).verify_convert() == 0
