def mapping(value, min_in, max_in, min_out, max_out):
    return (value - min_in) * (max_out - min_out)/(max_in - min_in) + min_out


if __name__ == "__main__":
    mapping()
