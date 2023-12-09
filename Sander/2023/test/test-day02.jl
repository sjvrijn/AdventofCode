using AdventofCode: day02

@testset "Day 2" begin

    @testset "Day 2, part 1" begin
        testfiles = Dict(
            "input02-test1.txt" => 8,
        )
        for (file, result) in testfiles
            data = day02.parse_file(joinpath(INPUT, file))
            @test day02.a(data) == result
        end
    end

    @testset "Day 2, part 2" begin
        testfiles = Dict(
            "input02-test1.txt" => 2286,
        )
        for (file, result) in testfiles
            data = day02.parse_file(joinpath(INPUT, file))
            @test day02.b(data) == result
        end
    end

end