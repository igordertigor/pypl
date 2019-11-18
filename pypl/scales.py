def linear_scale(rng_in, rng_out):
    x0, x1 = rng_in
    y0, y1 = rng_out
    a = (y1 - y0)/(x1 - x0)

    def f(x):
        return y0 + a*(x - x0)

    return f
